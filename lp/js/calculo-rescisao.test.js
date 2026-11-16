// Testes do cálculo de rescisão: node lp/js/calculo-rescisao.test.js
var assert = require('assert');
var c = require('./calculo-rescisao.js');

function caso(nome, fn) { try { fn(); console.log('ok   ' + nome); } catch (e) { console.log('FALHA ' + nome + ': ' + e.message); process.exitCode = 1; } }
function verba(r, chave) { var v = r.verbas.filter(function (x) { return x.chave === chave; })[0]; return v ? v.valor : 0; }
function desc(r, chave) { var v = r.descontos.filter(function (x) { return x.chave === chave; })[0]; return v ? v.valor : 0; }

caso('aviso prévio: 30 dias + 3 por ano completo, até 90', function () {
  assert.strictEqual(c.diasAviso('2026-01-10', '2026-06-10'), 30);
  assert.strictEqual(c.diasAviso('2020-01-10', '2026-06-10'), 48); // 6 anos completos
  assert.strictEqual(c.diasAviso('2020-06-11', '2026-06-10'), 45); // 5 anos completos
  assert.strictEqual(c.diasAviso('1990-01-01', '2026-06-10'), 90);
});

caso('férias proporcionais: meses do período aquisitivo, 15 dias contam', function () {
  assert.strictEqual(c.avosFerias('2024-03-01', '2026-06-14'), 3); // aquisitivo desde 01/03/2026: mar, abr, mai + 14 dias
  assert.strictEqual(c.avosFerias('2024-03-01', '2026-06-15'), 4); // + 15 dias conta
  assert.strictEqual(c.avosFerias('2026-01-05', '2026-01-25'), 1);
});

caso('saldo de salário: dias trabalhados no mês da saída', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'pediu_demissao', admissao: '2024-03-01', saida: '2026-06-10', aviso: 'trabalhado' });
  assert.strictEqual(verba(r, 'saldo'), 1000);
});

caso('saída no último dia de fevereiro: salário inteiro', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'pediu_demissao', admissao: '2024-03-01', saida: '2026-02-28', aviso: 'trabalhado' });
  assert.strictEqual(verba(r, 'saldo'), 3000);
});

caso('demitido sem justa causa com aviso indenizado: aviso, projeção, multa de 40% e saque', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'sem_justa_causa', admissao: '2020-01-10', saida: '2026-06-10', aviso: 'indenizado', saldoFgts: 10000 });
  assert.strictEqual(r.diasAviso, 48);
  assert.strictEqual(verba(r, 'aviso'), 4800);
  assert.strictEqual(r.avos13, 7);                       // aviso projeta até 28/07
  assert.strictEqual(verba(r, 'decimo'), 1750);          // 3000 * 7/12
  assert.strictEqual(r.avosFerias, 7);                   // aquisitivo desde 10/01/2026, fim projetado 28/07 (10 a 28/07 = 19 dias, conta)
  assert.strictEqual(verba(r, 'ferias_prop'), 2333.33);  // 3000 * 7/12 * 4/3
  // FGTS da rescisão: 8% sobre saldo (1000), aviso (4800) e 13º (1750) = 604
  assert.strictEqual(r.fgts.depositoRescisao, 604);
  assert.strictEqual(r.fgts.multa, 4241.6);              // 40% de (10000 + 604)
  assert.strictEqual(r.fgts.saque, 14845.6);
  assert.ok(r.seguroDesemprego);
});

caso('pediu demissão sem cumprir o aviso: desconto de 30 dias, sem multa e sem saque', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'pediu_demissao', admissao: '2020-01-10', saida: '2026-06-10', aviso: 'nao_cumprido', saldoFgts: 10000 });
  assert.strictEqual(desc(r, 'aviso_nao_cumprido'), 3000);
  assert.strictEqual(verba(r, 'aviso'), 0);
  assert.strictEqual(r.fgts.multa, 0);
  assert.strictEqual(r.fgts.saque, 0);
  assert.ok(!r.seguroDesemprego);
  assert.ok(verba(r, 'ferias_prop') > 0);                // férias proporcionais também no pedido de demissão (Súmula 261 do TST)
});

caso('acordo: metade do aviso, multa de 20% e saque de 80%', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'acordo', admissao: '2020-01-10', saida: '2026-06-10', aviso: 'indenizado', saldoFgts: 10000 });
  assert.strictEqual(verba(r, 'aviso'), 2400);           // metade de 48 dias
  assert.strictEqual(r.fgts.multa, r2(0.2 * (10000 + r.fgts.depositoRescisao)));
  assert.strictEqual(r.fgts.saque, r2(0.8 * (10000 + r.fgts.depositoRescisao) + r.fgts.multa));
  assert.ok(!r.seguroDesemprego);
});

caso('justa causa: só saldo e férias vencidas', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'justa_causa', admissao: '2020-01-10', saida: '2026-06-10', feriasVencidas: 1 });
  assert.strictEqual(verba(r, 'saldo'), 1000);
  assert.strictEqual(verba(r, 'ferias_venc'), 4000);
  assert.strictEqual(verba(r, 'decimo'), 0);
  assert.strictEqual(verba(r, 'ferias_prop'), 0);
  assert.strictEqual(r.fgts.saque, 0);
});

caso('férias e aviso indenizados não têm INSS nem IR; saldo e 13º têm', function () {
  var r = c.calcularRescisao({ salario: 8000, situacao: 'sem_justa_causa', admissao: '2020-01-10', saida: '2026-06-30', aviso: 'indenizado' });
  assert.ok(desc(r, 'inss_saldo') > 0);
  assert.ok(desc(r, 'inss_13') > 0);
  assert.ok(desc(r, 'irrf_saldo') > 0);                  // R$ 8.000 de saldo passa da faixa de redução
  assert.strictEqual(r2(r.bruto - r.totalDescontos), r.liquido);
});

caso('adiantamento do 13º já recebido é descontado', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'sem_justa_causa', admissao: '2020-01-10', saida: '2026-12-10', aviso: 'trabalhado', primeiraJaRecebida: true });
  assert.strictEqual(desc(r, 'adiant_13'), 1500);
});

caso('prazo de pagamento: 10 dias após o fim do contrato', function () {
  var r = c.calcularRescisao({ salario: 3000, situacao: 'sem_justa_causa', admissao: '2020-01-10', saida: '2026-06-10', aviso: 'indenizado' });
  assert.strictEqual(r.prazoPagamento, '2026-06-20');
});

caso('gestante recebe aviso de estabilidade', function () {
  var r = c.calcularRescisao({ salario: 2000, situacao: 'sem_justa_causa', admissao: '2025-01-10', saida: '2026-06-10', aviso: 'indenizado', gestante: true });
  assert.ok(r.avisos.some(function (a) { return /estabilidade/i.test(a); }));
});

function r2(v) { return Math.round((v + 1e-9) * 100) / 100; }
