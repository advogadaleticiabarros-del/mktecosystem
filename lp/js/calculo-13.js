/* Cálculo do 13º salário 2026 (CLT e doméstica). Uma função pura, calcular13(entrada), usada pela LP
   lp/calculadora-13-salario.html e pelos testes (node lp/js/calculo-13.test.js).
   Fontes: Lei 4.090/1962 e 4.749/1965, Decreto 10.854/2021, CLT art. 487 e 484-A, Lei 12.506/2011,
   LC 150/2015 (doméstica), Portaria Interministerial MPS/MF 13/2026 (INSS), Lei 15.270/2025 (redução do IR). */
(function (raiz) {
  var SALARIO_MINIMO = 1621.00;
  // INSS 2026, progressivo por faixa (empregado e doméstica).
  var FAIXAS_INSS = [[1621.00, 0.075], [2902.84, 0.09], [4354.27, 0.12], [8475.55, 0.14]];
  // IRRF mensal (tabela vigente desde maio/2025, mantida em 2026): [limite, alíquota, parcela a deduzir].
  var FAIXAS_IR = [[2428.80, 0, 0], [2826.65, 0.075, 182.16], [3751.05, 0.15, 394.16], [4664.68, 0.225, 675.49], [Infinity, 0.275, 908.73]];
  var DEDUCAO_DEPENDENTE = 189.59;

  function r2(v) { return Math.round((v + 1e-9) * 100) / 100; }

  function inss(base) {
    var total = 0, anterior = 0;
    for (var i = 0; i < FAIXAS_INSS.length; i++) {
      var teto = FAIXAS_INSS[i][0];
      if (base <= anterior) break;
      total += (Math.min(base, teto) - anterior) * FAIXAS_INSS[i][1];
      anterior = teto;
    }
    return r2(total);
  }

  // Tributação exclusiva do 13º, com a redução da Lei 15.270/2025 calculada sobre o rendimento bruto.
  function irrf(bruto, descontoInss, dependentes) {
    var base = bruto - descontoInss - (dependentes || 0) * DEDUCAO_DEPENDENTE;
    if (base <= 0) return 0;
    var imposto = 0;
    for (var i = 0; i < FAIXAS_IR.length; i++) {
      if (base <= FAIXAS_IR[i][0]) { imposto = base * FAIXAS_IR[i][1] - FAIXAS_IR[i][2]; break; }
    }
    imposto = Math.max(0, imposto);
    var reducao = 0;
    if (bruto <= 5000) reducao = imposto;
    else if (bruto <= 7350) reducao = Math.max(0, 978.62 - 0.133145 * bruto);
    return r2(Math.max(0, imposto - reducao));
  }

  function data(s) { var p = String(s).split('-'); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
  function diasEntre(a, b) { return Math.round((b - a) / 86400000) + 1; }

  // Aviso prévio: 30 dias + 3 por ano completo, até 90 (Lei 12.506/2011).
  function diasAviso(admissao, saida) {
    var anos = saida.getUTCFullYear() - admissao.getUTCFullYear();
    if (saida.getUTCMonth() < admissao.getUTCMonth() ||
      (saida.getUTCMonth() === admissao.getUTCMonth() && saida.getUTCDate() < admissao.getUTCDate())) anos--;
    return Math.min(90, 30 + 3 * Math.max(0, anos));
  }

  // Um avo por mês do ano com 15 dias ou mais de contrato.
  function contarAvos(inicio, fim, ano) {
    var avos = 0;
    for (var m = 0; m < 12; m++) {
      var ini = new Date(Date.UTC(ano, m, 1)), ult = new Date(Date.UTC(ano, m + 1, 0));
      var a = inicio > ini ? inicio : ini, b = fim < ult ? fim : ult;
      if (b >= a && diasEntre(a, b) >= 15) avos++;
    }
    return avos;
  }

  /* entrada: {
       ano, salario, situacao: 'trabalhando'|'sem_justa_causa'|'pediu_demissao'|'acordo'|'justa_causa',
       admissao: 'AAAA-MM-DD', saida: 'AAAA-MM-DD' (se saiu), avisoIndenizado: bool,
       insalubridade: 0|10|20|40, periculosidade: bool, mediaVariaveis (horas extras, comissões, noturno),
       mesesAfastadoInss, mesesFaltas (meses com mais de 15 faltas sem justificativa),
       dependentes, primeiraJaRecebida: bool } */
  function calcular13(e) {
    var ano = e.ano || 2026;
    var salario = Number(e.salario) || 0;
    var avisos = [];
    var adicionais = 0;
    if (e.insalubridade) adicionais += SALARIO_MINIMO * e.insalubridade / 100;
    if (e.periculosidade) adicionais += salario * 0.30;
    var remuneracao = r2(salario + adicionais + (Number(e.mediaVariaveis) || 0));

    var saiu = e.situacao && e.situacao !== 'trabalhando';
    if (e.situacao === 'justa_causa') {
      return { avos: 0, remuneracao: remuneracao, bruto: 0, inss: 0, irrf: 0, liquido: 0, parcelas: [], rescisao: true,
        avisos: ['Na demissão por justa causa a lei não garante o 13º proporcional do ano. Vale conferir se a justa causa foi aplicada corretamente: é a punição mais grave e a empresa precisa provar o motivo.'] };
    }

    var inicioAno = new Date(Date.UTC(ano, 0, 1)), fimAno = new Date(Date.UTC(ano, 11, 31));
    var admissao = e.admissao ? data(e.admissao) : null;
    var inicio = admissao && admissao > inicioAno ? admissao : inicioAno;
    var fim = fimAno, diasProjetados = 0;
    if (saiu && e.saida) {
      fim = data(e.saida);
      if (e.avisoIndenizado && (e.situacao === 'sem_justa_causa' || e.situacao === 'acordo')) {
        diasProjetados = admissao ? diasAviso(admissao, fim) : 30;
        if (e.situacao === 'acordo') diasProjetados = Math.floor(diasProjetados / 2);
        fim = new Date(fim.getTime() + diasProjetados * 86400000);
        if (fim > fimAno) fim = fimAno;
        avisos.push('O aviso prévio indenizado de ' + diasProjetados + ' dias conta como tempo de serviço e pode somar meses ao 13º.');
      }
    }

    var avosContrato = contarAvos(inicio, fim, ano);
    var avos = Math.max(0, avosContrato - (Number(e.mesesAfastadoInss) || 0) - (Number(e.mesesFaltas) || 0));
    if (e.mesesAfastadoInss > 0) avisos.push('Nos meses em que você recebeu auxílio do INSS, quem paga essa parte é o INSS (abono anual), não a empresa.');
    if (e.mesesFaltas > 0) avisos.push('Só tiram o mês do 13º as faltas sem justificativa que passem de 15 no mês. Atestado médico, férias e licença-maternidade não descontam.');
    if (e.mediaVariaveis > 0) avisos.push('Horas extras, comissões e adicional noturno entram pela média do ano. Se a empresa não somou, a diferença é devida.');

    var bruto = r2(remuneracao * avos / 12);
    var descInss = inss(bruto);
    var descIr = irrf(bruto, descInss, Number(e.dependentes) || 0);
    var liquido = r2(bruto - descInss - descIr);
    var res = { avos: avos, remuneracao: remuneracao, bruto: bruto, inss: descInss, irrf: descIr, liquido: liquido,
      parcelas: [], rescisao: !!saiu, diasAviso: diasProjetados, avisos: avisos };

    if (saiu) {
      if (e.primeiraJaRecebida) {
        res.parcelas.push({ nome: 'Já recebido (1ª parcela)', valor: r2(bruto / 2) });
        res.parcelas.push({ nome: 'A receber na rescisão', valor: r2(liquido - bruto / 2) });
      } else {
        res.parcelas.push({ nome: 'Na rescisão (até 10 dias após a saída)', valor: liquido });
      }
      return res;
    }
    var primeira = r2(bruto / 2);
    res.parcelas.push({ nome: e.primeiraJaRecebida ? '1ª parcela (já recebida, ex.: nas férias)' : '1ª parcela, até 30/11/' + ano, valor: primeira, semDesconto: true });
    res.parcelas.push({ nome: '2ª parcela, até 18/12/' + ano + ' (dia 20 cai num domingo)', valor: r2(liquido - primeira) });
    return res;
  }

  var api = { calcular13: calcular13, inss: inss, irrf: irrf, contarAvos: contarAvos };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else raiz.Calculo13 = api;
})(this);
