// Mundo 3D em miniatura dos Reels da Letícia (motor3d, 15/10/2026).
// Argila clara + ouro sobre café escuro. Tudo é função do tempo t (determinístico): o render quadro a quadro
// chama atualizar(t) e o mesmo t sempre desenha o mesmo quadro.
import * as THREE from "three";
import { RoomEnvironment } from "roomenv";

const OURO = 0xf0cd82, ARGILA = 0xe8ded1, ARGILA2 = 0xb9ad9f, CAFE = 0x1a1511;

const em = (o, x, y, z) => { o.position.set(x, y, z); return o; };
const suave = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const lerp = (a, b, k) => a + (b - a) * k;

// Trilha: lista de [t, valor]; interpola com suavização entre chaves.
export function valor(trilha, t, padrao = 0) {
  if (!trilha || !trilha.length) return padrao;
  if (t <= trilha[0][0]) return trilha[0][1];
  for (let i = 1; i < trilha.length; i++) {
    const [t0, v0] = trilha[i - 1], [t1, v1] = trilha[i];
    if (t <= t1) {
      const k = suave((t - t0) / Math.max(1e-6, t1 - t0));
      return Array.isArray(v0) ? v0.map((x, j) => lerp(x, v1[j], k)) : lerp(v0, v1, k);
    }
  }
  return trilha.at(-1)[1];
}

function rotulo(texto, cor = "#3a2f26", tam = 64) {
  const c = document.createElement("canvas");
  c.width = 256; c.height = 128;
  const g = c.getContext("2d");
  g.fillStyle = cor; g.font = `800 ${tam}px Inter, sans-serif`; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillText(texto, 128, 66);
  const tex = new THREE.CanvasTexture(c);
  tex.anisotropy = 4;
  return new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.25), new THREE.MeshBasicMaterial({ map: tex, transparent: true }));
}

function papel(titulo, linhas) {
  const c = document.createElement("canvas");
  c.width = 512; c.height = 680;
  const g = c.getContext("2d");
  g.fillStyle = "#f6f0e6"; g.fillRect(0, 0, 512, 680);
  g.fillStyle = "#8E6E2E"; g.font = "800 38px Inter, sans-serif"; g.fillText(titulo, 36, 72);
  g.fillStyle = "#c9bfb2";
  for (let i = 0; i < linhas; i++) g.fillRect(36, 120 + i * 46, 300 + ((i * 97) % 140), 14);
  g.fillStyle = "#C9A962"; g.fillRect(36, 600, 180, 18);
  const tex = new THREE.CanvasTexture(c);
  const m = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.02, 1.46), [
    new THREE.MeshStandardMaterial({ color: 0xf6f0e6 }), new THREE.MeshStandardMaterial({ color: 0xf6f0e6 }),
    new THREE.MeshStandardMaterial({ map: tex, roughness: 0.8 }), new THREE.MeshStandardMaterial({ color: 0xe9e1d4 }),
    new THREE.MeshStandardMaterial({ color: 0xf6f0e6 }), new THREE.MeshStandardMaterial({ color: 0xf6f0e6 })]);
  m.castShadow = true;
  return m;
}

export function criarMundo(canvas, L, A) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(L, A, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const cena = new THREE.Scene();
  cena.background = new THREE.Color(CAFE);
  cena.fog = new THREE.Fog(CAFE, 32, 75);
  const pmrem = new THREE.PMREMGenerator(renderer);
  cena.environment = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;

  const camera = new THREE.PerspectiveCamera(30, L / A, 0.1, 120);
  cena.add(new THREE.HemisphereLight(0xfff3e0, 0x2a2018, 0.55));
  const sol = new THREE.DirectionalLight(0xffe2b8, 2.2);
  sol.position.set(6, 12, 8);
  sol.castShadow = true;
  sol.shadow.mapSize.set(2048, 2048);
  Object.assign(sol.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16, near: 1, far: 50 });
  sol.shadow.radius = 4;
  cena.add(sol, sol.target);

  const mArg = new THREE.MeshStandardMaterial({ color: ARGILA, roughness: 0.55 });
  const mArg2 = new THREE.MeshStandardMaterial({ color: ARGILA2, roughness: 0.7 });
  const mOuro = new THREE.MeshStandardMaterial({ color: OURO, metalness: 0.9, roughness: 0.3, envMapIntensity: 1.8, emissive: 0x3a2808, emissiveIntensity: 0.35 });
  const mCafe = new THREE.MeshStandardMaterial({ color: 0x3a2e25, roughness: 0.6 });
  const caixa = (w, h, d, m) => { const x = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); x.castShadow = x.receiveShadow = true; return x; };

  const chao = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshStandardMaterial({ color: 0x241c16, roughness: 1 }));
  chao.rotation.x = -Math.PI / 2; chao.receiveShadow = true; cena.add(chao);

  // --- Semana (x = 0): 7 pilares SEG..DOM; altura = horas do dia; folga = pilar baixo em ouro.
  const semana = new THREE.Group(); cena.add(semana);
  semana.add(em(caixa(5.8, 0.25, 1.4, mArg2), 0, 0.125, 0));
  const dias = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"];
  const pilares = dias.map((d, i) => {
    const p = caixa(0.5, 1, 0.5, mArg.clone()); p.position.set(-2.4 + i * 0.8, 0.75, 0); semana.add(p);
    const r = rotulo(d, i >= 5 ? "#8E6E2E" : "#3a2f26", 58); r.position.set(-2.4 + i * 0.8, 0.13, 0.71); semana.add(r);
    return p;
  });

  // --- Congresso (x = 9): plataforma, torres gêmeas, cúpula e "bacia".
  const cong = new THREE.Group(); cong.position.set(9, 0, 0); cena.add(cong);
  cong.add(em(caixa(6.4, 0.35, 2.6, mArg), 0, 0.175, 0));
  [-0.32, 0.32].forEach((x) => cong.add(em(caixa(0.5, 3.6, 0.55, mArg), x, 2.15, -0.6)));
  cong.add(em(caixa(1.15, 0.12, 0.6, mArg), 0, 3.2, -0.6));
  const cupula = new THREE.Mesh(new THREE.SphereGeometry(0.85, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), mArg);
  cupula.position.set(-2, 0.35, 0.3); cupula.castShadow = true; cong.add(cupula);
  const bacia = new THREE.Mesh(new THREE.SphereGeometry(1.05, 48, 24, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), mArg);
  bacia.position.set(2, 1.25, 0.3); bacia.castShadow = true; cong.add(bacia);
  cong.add(em(new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 0.9, 24), mArg), 2, 0.8, 0.3));
  // Carimbo dourado que desce sobre a plataforma.
  const carimbo = new THREE.Group(); cong.add(carimbo);
  carimbo.add(em(caixa(1.1, 0.3, 0.7, mOuro), 0, 0, 0));
  carimbo.add(em(new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.7, 24), mCafe), 0, 0.5, 0));
  carimbo.add(em(new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 16), mCafe), 0, 0.95, 0));

  // --- Constituição e mesa (x = 18).
  const consti = new THREE.Group(); consti.position.set(18, 0, 0); cena.add(consti);
  const mesa = new THREE.Group(); consti.add(mesa);
  mesa.add(em(caixa(3.2, 0.14, 1.8, mCafe), 0, 1.1, 0));
  [[-1.45, -0.75], [1.45, -0.75], [-1.45, 0.75], [1.45, 0.75]].forEach(([x, z]) => mesa.add(em(caixa(0.12, 1.05, 0.12, mCafe), x, 0.52, z)));
  const livro = new THREE.Group(); livro.position.set(0, 1.2, 0); consti.add(livro);
  livro.add(em(caixa(1.4, 0.12, 1.0, mArg), 0, 0.06, 0));
  const capa = new THREE.Group(); capa.position.set(-0.72, 0.13, 0); livro.add(capa);
  const capaM = caixa(1.44, 0.04, 1.04, new THREE.MeshStandardMaterial({ color: 0x5a3f22, roughness: 0.5 })); capaM.position.set(0.72, 0, 0); capa.add(capaM);
  const brasao = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.02, 32), mOuro); brasao.position.set(0.72, 0.03, 0); capa.add(brasao);
  const caneta = em(new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.9, 16), mOuro), 1.1, 1.3, 0.35);
  caneta.rotation.z = Math.PI / 2.4; caneta.castShadow = true; consti.add(caneta);

  // --- Salário e documentos (x = -8): pilha de moedas e papéis.
  const cofre = new THREE.Group(); cofre.position.set(-8, 0, 0); cena.add(cofre);
  const moedas = Array.from({ length: 9 }, (_, i) => {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.11, 48), mOuro); m.castShadow = true;
    m.position.set(-0.9 + (i % 3) * 0.05, 0.06 + i * 0.12, (i % 2) * 0.04); cofre.add(m); return m;
  });
  const p1 = papel("CONTRACHEQUE", 9), p2 = papel("ESPELHO DE PONTO", 10);
  p1.position.set(0.8, 0.02, 0.1); p1.rotation.y = 0.12; p2.position.set(1.4, 0.05, -0.3); p2.rotation.y = -0.18;
  cofre.add(p1, p2);

  // --- Pó de ouro flutuando (deterministico).
  const N = 420, pos = new Float32Array(N * 3), base = [];
  for (let i = 0; i < N; i++) {
    const s = Math.sin(i * 12.9898) * 43758.5453, r = s - Math.floor(s);
    const s2 = Math.sin(i * 78.233) * 12345.678, r2 = s2 - Math.floor(s2);
    const s3 = Math.sin(i * 39.425) * 9876.543, r3 = s3 - Math.floor(s3);
    base.push([-14 + r * 40, 0.3 + r2 * 7, -6 + r3 * 9, r * 6.28]);
  }
  const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const po = new THREE.Points(geo, new THREE.PointsMaterial({ color: 0xf2d79a, size: 0.05, transparent: true, opacity: 0.85, depthWrite: false }));
  cena.add(po);

  const projetar = (v) => {
    const p = new THREE.Vector3(...v).project(camera);
    return [(p.x + 1) / 2 * L, (1 - p.y) / 2 * A];
  };

  function atualizar(t, R) {
    const tr = R.trilhas;
    // câmera
    const cam = valor(R.camera.map(([tt, p]) => [tt, p]), t);
    camera.position.set(cam[0], cam[1], cam[2]);
    camera.lookAt(cam[3], cam[4], cam[5]);
    // semana: subir (0..1), horas por dia (escala), folga do sábado (0..1)
    const sobe = valor(tr.semana_sobe, t, 1), horas = valor(tr.horas, t, 1), sab = valor(tr.sabado_folga, t, 0);
    pilares.forEach((p, i) => {
      const k = suave((sobe * 7 - i) / 1.2);
      let h = i === 6 ? 0.35 : 1.6 * horas;
      if (i === 5) h = lerp(1.6 * horas, 0.35, sab);
      const hh = Math.max(0.02, h * k);
      p.scale.y = hh; p.position.y = 0.25 + hh / 2;
      const ouro = i === 6 ? 1 : i === 5 ? sab : 0;
      p.material.color.setHex(ouro > 0.5 ? OURO : ARGILA);
      p.material.metalness = 0.9 * ouro; p.material.roughness = lerp(0.55, 0.3, ouro); p.material.envMapIntensity = lerp(1, 1.8, ouro); p.material.emissive.setHex(ouro > 0.5 ? 0x3a2808 : 0x000000); p.material.emissiveIntensity = 0.35;
    });
    // carimbo: desce (0 alto .. 1 encostado) e some
    const c = valor(tr.carimbo, t, 0);
    carimbo.position.set(0, lerp(5.5, 0.52, c), 0.9);
    carimbo.visible = valor(tr.carimbo_vis, t, 0) > 0.5;
    // livro: abre capa (0..1); caneta assina
    capa.rotation.z = lerp(0, Math.PI * 0.92, valor(tr.livro_abre, t, 0));
    caneta.position.x = 1.1 - 0.8 * valor(tr.assina, t, 0);
    // moedas sobem (0..1); papéis surgem (0..1)
    const m = valor(tr.moedas, t, 0);
    moedas.forEach((mo, i) => { const k = suave(m * 9 - i); mo.position.y = 0.06 + i * 0.12 + (1 - k) * 4; mo.visible = k > 0.01; });
    const pp = valor(tr.papeis, t, 0);
    p1.visible = p2.visible = pp > 0.001;
    p1.position.y = 0.02 + (1 - suave(pp * 2)) * 3; p2.position.y = 0.05 + (1 - suave(pp * 2 - 0.6)) * 3;
    // pó de ouro
    for (let i = 0; i < N; i++) {
      const [x, y, z, f] = base[i];
      pos[i * 3] = x + Math.sin(t * 0.21 + f) * 0.4; pos[i * 3 + 1] = y + Math.sin(t * 0.37 + f * 2) * 0.35; pos[i * 3 + 2] = z + Math.cos(t * 0.19 + f) * 0.3;
    }
    geo.attributes.position.needsUpdate = true;
    renderer.render(cena, camera);
  }

  return { atualizar, projetar };
}
