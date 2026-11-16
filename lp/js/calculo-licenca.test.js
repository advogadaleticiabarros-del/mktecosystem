// Testes das datas da licença-maternidade: node lp/js/calculo-licenca.test.js
var assert = require('assert');
var c = require('./calculo-licenca.js');

function caso(nome, fn) { try { fn(); console.log('ok   ' + nome); } catch (e) { console.log('FALHA ' + nome + ': ' + e.message); process.exitCode = 1; } }

caso('120 dias a partir do parto', function () {
  var r = c.calcularLicenca({ tipo: 'parto', data: '2026-03-01' });
  assert.strictEqual(r.inicio, '2026-03-01');
  assert.strictEqual(r.fim, '2026-06-28');       // 1º de março + 119 dias
  assert.strictEqual(r.retorno, '2026-06-29');
  assert.strictEqual(r.dias, 120);
});

caso('Empresa Cidadã: 180 dias e prazo para pedir a prorrogação', function () {
  var r = c.calcularLicenca({ tipo: 'parto', data: '2026-03-01', empresaCidada: true });
  assert.strictEqual(r.dias, 180);
  assert.strictEqual(r.fim, '2026-08-27');
  assert.strictEqual(r.fim120, '2026-06-28');
  assert.strictEqual(r.prazoProrrogacao, '2026-04-01');
});

caso('início antecipado em até 28 dias antes do parto', function () {
  var r = c.calcularLicenca({ tipo: 'parto', data: '2026-03-01', diasAntes: 28 });
  assert.strictEqual(r.inicio, '2026-02-01');
  assert.strictEqual(r.fim, '2026-05-31');
  var limite = c.calcularLicenca({ tipo: 'parto', data: '2026-03-01', diasAntes: 40 });
  assert.strictEqual(limite.inicio, '2026-02-01');  // nunca mais de 28 dias
});

caso('estabilidade até 5 meses depois do parto', function () {
  assert.strictEqual(c.calcularLicenca({ tipo: 'parto', data: '2026-03-31' }).fimEstabilidade, '2026-08-31');
  assert.strictEqual(c.calcularLicenca({ tipo: 'parto', data: '2026-09-30' }).fimEstabilidade, '2027-02-28'); // fevereiro sem dia 30
});

caso('amamentação: duas pausas de 30 minutos até o bebê fazer 6 meses', function () {
  assert.strictEqual(c.calcularLicenca({ tipo: 'parto', data: '2026-03-01' }).fimAmamentacao, '2026-09-01');
});

caso('internação de mais de 2 semanas: conta a partir da alta (ADI 6327)', function () {
  var r = c.calcularLicenca({ tipo: 'parto', data: '2026-03-01', alta: '2026-03-25' });
  assert.strictEqual(r.inicio, '2026-03-25');
  assert.strictEqual(r.fim, '2026-07-22');
  assert.ok(r.contaDaAlta);
  var curta = c.calcularLicenca({ tipo: 'parto', data: '2026-03-01', alta: '2026-03-10' }); // 9 dias: regra normal
  assert.strictEqual(curta.inicio, '2026-03-01');
  assert.ok(!curta.contaDaAlta);
});

caso('adoção: mesmos 120 dias a partir da guarda e estabilidade de 5 meses', function () {
  var r = c.calcularLicenca({ tipo: 'adocao', data: '2026-05-10' });
  assert.strictEqual(r.inicio, '2026-05-10');
  assert.strictEqual(r.dias, 120);
  assert.strictEqual(r.fimEstabilidade, '2026-10-10');
  assert.strictEqual(r.fimAmamentacao, null);
});
