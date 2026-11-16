/* Cálculo de rescisão CLT (estimativa). Uma função pura, calcularRescisao(entrada), usada pela LP
   lp/calculadora-rescisao.html e pelos testes (node lp/js/calculo-rescisao.test.js).
   Reaproveita INSS, IR e contagem de avos do 13º (lp/js/calculo-13.js, carregado antes na página).
   Fontes: CLT arts. 146, 477, 484-A e 487; Lei 12.506/2011 (aviso proporcional); Lei 8.036/1990 art. 18 e
   Decreto 99.684/1990 (FGTS e multa); Súmulas 171, 261 e 305 do TST; OJ 195 da SDI-1 do TST;
   Lei 7.713/1988 art. 6º, V e Súmula 386 do STJ (indenizações sem IR). */
(function (raiz) {
  var C13 = (typeof module !== 'undefined' && module.exports) ? require('./calculo-13.js') : raiz.Calculo13;
  var SALARIO_MINIMO = 1621.00;

  function r2(v) { return Math.round((v + 1e-9) * 100) / 100; }
  function data(s) { var p = String(s).split('-'); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
  function iso(d) { return d.toISOString().slice(0, 10); }
  function somaDias(d, n) { return new Date(d.getTime() + n * 86400000); }
  function somaMeses(d, n) {
    var a = d.getUTCFullYear(), m = d.getUTCMonth() + n, dia = d.getUTCDate();
    var ult = new Date(Date.UTC(a, m + 1, 0)).getUTCDate();
    return new Date(Date.UTC(a, m, Math.min(dia, ult)));
  }
  function anosCompletos(adm, fim) {
    var anos = fim.getUTCFullYear() - adm.getUTCFullYear();
    if (fim.getUTCMonth() < adm.getUTCMonth() || (fim.getUTCMonth() === adm.getUTCMonth() && fim.getUTCDate() < adm.getUTCDate())) anos--;
    return Math.max(0, anos);
  }

  // Aviso prévio do empregador: 30 dias + 3 por ano completo, até 90 (Lei 12.506/2011).
  function diasAviso(admissao, saida) {
    return Math.min(90, 30 + 3 * anosCompletos(data(admissao), data(saida)));
  }

  // Férias proporcionais: meses do período aquisitivo em curso; fração de 15 dias ou mais conta (CLT art. 146).
  function avosFerias(admissao, fim) {
    var adm = data(admissao), f = data(fim);
    var inicio = somaMeses(adm, 12 * anosCompletos(adm, f));
    var avos = 0, cursor = inicio;
    while (avos < 12 && somaDias(somaMeses(cursor, 1), -1) <= f) { avos++; cursor = somaMeses(cursor, 1); }
    if (avos < 12 && Math.round((f - cursor) / 86400000) + 1 >= 15) avos++;
    return avos;
  }

  /* entrada: {
       salario, situacao: 'sem_justa_causa'|'pediu_demissao'|'acordo'|'justa_causa',
       admissao: 'AAAA-MM-DD', saida: 'AAAA-MM-DD' (último dia trabalhado),
       aviso: 'trabalhado'|'indenizado'|'nao_cumprido'|'dispensado',
       feriasVencidas: 0|1|2, saldoFgts (opcional), insalubridade: 0|10|20|40, periculosidade,
       mediaVariaveis, dependentes, primeiraJaRecebida, gestante } */
  function calcularRescisao(e) {
    var s = e.situacao, salario = Number(e.salario) || 0;
    var adicionais = 0;
    if (e.insalubridade) adicionais += SALARIO_MINIMO * e.insalubridade / 100;
    if (e.periculosidade) adicionais += salario * 0.30;
    var rem = r2(salario + adicionais + (Number(e.mediaVariaveis) || 0));
    var adm = data(e.admissao), saida = data(e.saida);
    var verbas = [], descontos = [], avisos = [];
    function v(chave, nome, valor, nota) { if (valor > 0) verbas.push({ chave: chave, nome: nome, valor: r2(valor), nota: nota || '' }); }
    function d(chave, nome, valor) { if (valor > 0) descontos.push({ chave: chave, nome: nome, valor: r2(valor) }); }

    // Saldo de salário: dias trabalhados no mês da saída (mês comercial de 30 dias).
    var inicioMes = new Date(Date.UTC(saida.getUTCFullYear(), saida.getUTCMonth(), 1));
    var diasSaldo = Math.min(30, saida.getUTCDate() - (adm > inicioMes ? adm.getUTCDate() - 1 : 0));
    var ultimoDiaMes = somaDias(saida, 1).getUTCDate() === 1;
    if (ultimoDiaMes && adm <= inicioMes) diasSaldo = 30; // mês completo trabalhado = salário inteiro, inclusive em fevereiro
    var saldo = r2(rem / 30 * diasSaldo);
    v('saldo', 'Saldo de salário (' + diasSaldo + ' dias)', saldo);

    // Aviso prévio.
    var dias = diasAviso(e.admissao, e.saida), projecao = 0, valorAviso = 0;
    if (e.aviso === 'indenizado' && (s === 'sem_justa_causa' || s === 'acordo')) {
      projecao = s === 'acordo' ? Math.floor(dias / 2) : dias;
      valorAviso = rem / 30 * (s === 'acordo' ? dias / 2 : dias);
      v('aviso', 'Aviso prévio indenizado (' + (s === 'acordo' ? 'metade de ' + dias : dias) + ' dias)', valorAviso);
    }
    if (s === 'pediu_demissao' && e.aviso === 'nao_cumprido') {
      d('aviso_nao_cumprido', 'Aviso prévio não cumprido (30 dias)', salario);
      avisos.push('Quem pede demissão e não cumpre o aviso pode ter 30 dias de salário descontados. Se a empresa dispensou o aviso, não pode descontar.');
    }
    var fimProjetado = somaDias(saida, projecao);
    if (projecao) avisos.push('O aviso indenizado de ' + projecao + ' dias conta como tempo de serviço: soma meses no 13º e nas férias.');

    // 13º proporcional do ano da saída.
    var ano = saida.getUTCFullYear(), fimAno = new Date(Date.UTC(ano, 11, 31)), inicioAno = new Date(Date.UTC(ano, 0, 1));
    var avos13 = 0, decimo = 0;
    if (s !== 'justa_causa') {
      avos13 = C13.contarAvos(adm > inicioAno ? adm : inicioAno, fimProjetado > fimAno ? fimAno : fimProjetado, ano);
      decimo = r2(rem * avos13 / 12);
      v('decimo', '13º proporcional (' + avos13 + '/12)', decimo);
      if (e.primeiraJaRecebida) d('adiant_13', 'Adiantamento do 13º já recebido', rem / 2);
    }

    // Férias.
    var vencidas = Math.max(0, Math.min(2, Number(e.feriasVencidas) || 0));
    if (vencidas) {
      v('ferias_venc', 'Férias vencidas + 1/3 (' + vencidas + (vencidas > 1 ? ' períodos)' : ' período)'), rem * vencidas * 4 / 3);
      avisos.push('Férias vencidas que passaram do prazo de concessão (12 meses depois de completar o período) são pagas em dobro (CLT art. 137). A calculadora mostra o valor simples.');
    }
    var avosF = 0;
    if (s !== 'justa_causa') {
      avosF = avosFerias(e.admissao, iso(fimProjetado));
      v('ferias_prop', 'Férias proporcionais + 1/3 (' + avosF + '/12)', rem * avosF / 12 * 4 / 3);
    }

    // Descontos legais: INSS e IR só sobre saldo e 13º; aviso e férias indenizados ficam de fora.
    var dep = Number(e.dependentes) || 0;
    var inssSaldo = C13.inss(saldo), inss13 = C13.inss(decimo);
    d('inss_saldo', 'INSS sobre o saldo de salário', inssSaldo);
    d('inss_13', 'INSS sobre o 13º', inss13);
    d('irrf_saldo', 'Imposto de Renda sobre o saldo', C13.irrf(saldo, inssSaldo, dep));
    d('irrf_13', 'Imposto de Renda sobre o 13º', C13.irrf(decimo, inss13, dep));

    var bruto = r2(verbas.reduce(function (t, x) { return t + x.valor; }, 0));
    var totalDescontos = r2(descontos.reduce(function (t, x) { return t + x.valor; }, 0));

    // FGTS: depósito sobre saldo, aviso e 13º (não sobre férias indenizadas); multa e saque conforme a saída.
    var mesesContrato = Math.max(0, Math.round((saida - adm) / (86400000 * 30.4375)));
    var saldoInformado = Number(e.saldoFgts) > 0;
    var saldoFgts = saldoInformado ? r2(Number(e.saldoFgts)) : r2(0.08 * rem * mesesContrato);
    var deposito = r2(0.08 * (saldo + r2(valorAviso) + decimo));
    var base = r2(saldoFgts + deposito);
    var multa = s === 'sem_justa_causa' ? r2(base * 0.4) : s === 'acordo' ? r2(base * 0.2) : 0;
    var saque = s === 'sem_justa_causa' ? r2(base + multa) : s === 'acordo' ? r2(base * 0.8 + multa) : 0;
    if (!saldoInformado) avisos.push('O saldo do FGTS foi estimado em 8% da remuneração por mês de contrato, sem correção. O valor exato está no app FGTS.');
    if (s === 'sem_justa_causa' || s === 'acordo') avisos.push('Quem aderiu ao saque-aniversário não saca o saldo na demissão, só a multa.');
    if (s === 'pediu_demissao' || s === 'justa_causa') avisos.push('O FGTS continua na sua conta: nesta saída não há multa nem saque.');
    if (s === 'sem_justa_causa') avisos.push('Na dispensa sem justa causa você pode ter direito ao seguro-desemprego, conforme o tempo trabalhado.');
    if (s === 'acordo') avisos.push('No acordo (CLT art. 484-A) não há seguro-desemprego.');
    if (s === 'justa_causa') avisos.push('Na justa causa a lei tira o 13º, as férias proporcionais, o aviso e a multa do FGTS. É a punição mais grave: a empresa precisa provar o motivo, e vale conferir se foi aplicada corretamente.');
    if (e.gestante) avisos.push('Grávida não pode ser demitida sem justa causa desde a confirmação da gravidez até 5 meses após o parto, mesmo que a empresa não soubesse (estabilidade da gestante). Nesse caso cabe pedir a volta ao trabalho ou a indenização do período, além destas verbas.');

    return {
      remuneracao: rem, verbas: verbas, descontos: descontos, bruto: bruto, totalDescontos: totalDescontos,
      liquido: r2(bruto - totalDescontos), diasAviso: dias, projecao: projecao, avos13: avos13, avosFerias: avosF,
      fgts: { saldo: saldoFgts, estimado: !saldoInformado, depositoRescisao: deposito, multa: multa, saque: saque },
      prazoPagamento: iso(somaDias(saida, 10)), seguroDesemprego: s === 'sem_justa_causa', avisos: avisos
    };
  }

  var api = { calcularRescisao: calcularRescisao, diasAviso: diasAviso, avosFerias: avosFerias };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else raiz.CalculoRescisao = api;
})(this);
