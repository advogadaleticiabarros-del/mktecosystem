// Testes do cálculo do 13º: node lp/js/calculo-13.test.js
var assert = require('assert');
var c = require('./calculo-13.js');

function caso(nome, fn) { try { fn(); console.log('ok   ' + nome); } catch (e) { console.log('FALHA ' + nome + ': ' + e.message); process.exitCode = 1; } }

caso('INSS do salário mínimo é 7,5%', function () { assert.strictEqual(c.inss(1621), 121.58); });
caso('INSS no teto é R$ 988,09', function () { assert.strictEqual(c.inss(8475.55), 988.09); assert.strictEqual(c.inss(20000), 988.09); });
caso('IR do exemplo da Lei 15.270 (R$ 5.900, INSS 635,60) dá 345,92', function () { assert.strictEqual(c.irrf(5900, 635.60, 0), 345.92); });
caso('até R$ 5.000 o IR do 13º é zero', function () { assert.strictEqual(c.irrf(5000, c.inss(5000), 0), 0); });
caso('acima de R$ 7.350 não há redução', function () { assert.strictEqual(c.irrf(10000, 988.09, 0), r(9011.91 * 0.275 - 908.73)); });
function r(v) { return Math.round(v * 100) / 100; }

caso('ano inteiro: 12/12 e duas parcelas', function () {
  var x = c.calcular13({ salario: 3000, situacao: 'trabalhando' });
  assert.strictEqual(x.avos, 12); assert.strictEqual(x.bruto, 3000);
  assert.strictEqual(x.parcelas[0].valor, 1500);
  assert.strictEqual(r(x.parcelas[0].valor + x.parcelas[1].valor), x.liquido);
});
caso('admitido em março: 15 dias contam o mês, 14 não', function () {
  assert.strictEqual(c.calcular13({ salario: 1200, situacao: 'trabalhando', admissao: '2026-03-17' }).avos, 10); // 15 dias em março conta
  assert.strictEqual(c.calcular13({ salario: 1200, situacao: 'trabalhando', admissao: '2026-03-18' }).avos, 9);
});
caso('demitido sem justa causa projeta o aviso', function () {
  var sem = c.calcular13({ salario: 2400, situacao: 'pediu_demissao', admissao: '2020-01-10', saida: '2026-06-10' });
  var com = c.calcular13({ salario: 2400, situacao: 'sem_justa_causa', admissao: '2020-01-10', saida: '2026-06-10', avisoIndenizado: true });
  assert.strictEqual(sem.avos, 5);
  assert.strictEqual(com.diasAviso, 48); // 6 anos completos
  assert.strictEqual(com.avos, 7); // até 28/07
});
caso('justa causa zera', function () { assert.strictEqual(c.calcular13({ salario: 2000, situacao: 'justa_causa' }).bruto, 0); });
caso('afastamento do INSS tira os meses', function () { assert.strictEqual(c.calcular13({ salario: 2000, situacao: 'trabalhando', mesesAfastadoInss: 3 }).avos, 9); });
caso('insalubridade grau médio soma 20% do mínimo', function () { assert.strictEqual(c.calcular13({ salario: 2000, situacao: 'trabalhando', insalubridade: 20 }).remuneracao, 2324.2); });
