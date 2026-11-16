/* Datas da licença-maternidade (CLT). Uma função pura, calcularLicenca(entrada), usada pela LP
   lp/calculadora-licenca-maternidade.html e pelos testes (node lp/js/calculo-licenca.test.js).
   Fontes: CF art. 7º, XVIII; ADCT art. 10, II, b; CLT arts. 391-A, 392, 392-A e 396; Lei 11.770/2008
   (Empresa Cidadã); STF ADI 6327 (contagem a partir da alta) e ADI 7.495 (adotante, 23/09/2026). */
(function (raiz) {
  function data(s) { var p = String(s).split('-'); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
  function iso(d) { return d.toISOString().slice(0, 10); }
  function somaDias(d, n) { return new Date(d.getTime() + n * 86400000); }
  function somaMeses(d, n) {
    var a = d.getUTCFullYear(), m = d.getUTCMonth() + n, dia = d.getUTCDate();
    var ult = new Date(Date.UTC(a, m + 1, 0)).getUTCDate();
    return new Date(Date.UTC(a, m, Math.min(dia, ult)));
  }

  /* entrada: { tipo: 'parto'|'adocao', data: 'AAAA-MM-DD' (parto, previsto ou ocorrido, ou guarda para adoção),
       diasAntes: 0..28 (só parto), empresaCidada: bool, alta: 'AAAA-MM-DD' (alta da mãe ou do bebê, a mais tardia) } */
  function calcularLicenca(e) {
    var evento = data(e.data), parto = e.tipo !== 'adocao';
    var dias = e.empresaCidada ? 180 : 120;
    var inicio = evento, contaDaAlta = false;
    if (parto) {
      var antes = Math.max(0, Math.min(28, Number(e.diasAntes) || 0));
      inicio = somaDias(evento, -antes);
      if (e.alta) {
        var alta = data(e.alta);
        if (Math.round((alta - evento) / 86400000) > 14) { inicio = alta; contaDaAlta = true; }
      }
    }
    var fim = somaDias(inicio, dias - 1);
    return {
      tipo: parto ? 'parto' : 'adocao', dias: dias,
      inicio: iso(inicio), fim: iso(fim), retorno: iso(somaDias(fim, 1)),
      fim120: iso(somaDias(inicio, 119)),
      prazoProrrogacao: e.empresaCidada ? iso(somaMeses(evento, 1)) : null,
      fimEstabilidade: iso(somaMeses(evento, 5)),
      fimAmamentacao: parto ? iso(somaMeses(evento, 6)) : null,
      contaDaAlta: contaDaAlta
    };
  }

  var api = { calcularLicenca: calcularLicenca };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else raiz.CalculoLicenca = api;
})(this);
