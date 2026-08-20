(function () {
  'use strict';
  const T = window.Tools, $ = id => document.getElementById(id);
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const clean = (s, n) => (String(s).replace(/[^01]/g, '') || '0').slice(-n).padStart(n, '0');
  const dec = b => parseInt(b, 2) || 0;

  /* ---------- STEP1 加算 ---------- */
  let addPos = 0;
  function addCalc() {
    const N = 8;
    const a = clean($('addA').value, N), b = clean($('addB').value, N);
    const res = [], carry = [];
    let c = 0;
    for (let i = N - 1; i >= 0; i--) {
      const s = +a[i] + +b[i] + c;
      res[i] = s % 2; c = s >= 2 ? 1 : 0; carry[i] = c;
    }
    return { a, b, res, carry, over: c };
  }
  function drawAdd() {
    const N = 8, { a, b, res, carry, over } = addCalc();
    const shown = addPos;                        // 右から何桁計算したか
    const d = (ch, i, cls) => '<span class="d' + (cls || '') + '">' + ch + '</span>';
    let h = '<div class="row"><span class="lbl">くり上がり</span>';
    for (let i = 0; i < N; i++) {
      const from = i + 1;
      const show = (N - from) < shown && from < N ? carry[from] : '';
      h += d(show === '' ? '' : (show ? '1' : ''), i, ' carry' + ((N - 1 - i) === shown - 1 ? ' hi' : ''));
    }
    h += '</div>';
    h += '<div class="row"><span class="lbl"></span>' + [...a].map((ch, i) =>
      d(ch, i, (N - 1 - i) === shown - 1 ? ' hi' : '')).join('') + '</div>';
    h += '<div class="row"><span class="lbl">＋</span>' + [...b].map((ch, i) =>
      d(ch, i, (N - 1 - i) === shown - 1 ? ' hi' : '')).join('') + '</div>';
    h += '<div class="line"></div>';
    h += '<div class="row"><span class="lbl"></span>' + (over && shown >= N ? d('1', -1, ' hi') : '') +
      res.map((v, i) => (N - 1 - i) < shown ? d(v, i, (N - 1 - i) === shown - 1 ? ' hi' : '') : d('_', i)).join('') + '</div>';
    $('addGrid').innerHTML = h;
    const n = $('addNote');
    if (shown === 0) {
      n.className = 'note info';
      n.innerHTML = '<strong>いちばん右の位</strong>から計算します。「1桁ずつ進む」を押してください。';
    } else if (shown <= N) {
      const i = N - shown;
      const s = +a[i] + +b[i] + (shown > 1 ? carry[i + 1] : 0);
      n.className = 'note ' + (s >= 2 ? 'warn' : 'info');
      n.innerHTML = '右から ' + shown + ' 桁目：' + a[i] + ' ＋ ' + b[i] +
        (shown > 1 && carry[i + 1] ? ' ＋ くり上がり1' : '') + ' ＝ ' + s + '　→　' +
        (s >= 2 ? '<strong>' + (s % 2) + ' を書いて 1 くり上がる</strong>' : '<strong>' + s + '</strong> を書く');
    }
    if (shown >= N) {
      n.className = 'note ok';
      n.innerHTML = '計算が終わりました。答えは <strong>' + (over ? '1' : '') + res.join('') + '(2)</strong>' +
        (over ? '（8ビットからあふれました）' : '') + '。';
    }
    $('addCheck').innerHTML = dec(a) + ' ＋ ' + dec(b) + ' ＝ ' + (dec(a) + dec(b)) +
      '　（2進法：' + (over ? '1' : '') + res.join('') + '）';
  }

  /* ---------- STEP2 減算 ---------- */
  let subPos = 0;
  function subCalc() {
    const N = Math.max(clean($('subA').value, 8).replace(/^0+/, '').length,
      clean($('subB').value, 8).replace(/^0+/, '').length, 4);
    const a = clean($('subA').value, N), b = clean($('subB').value, N);
    const res = [], borrow = [];
    let br = 0;
    for (let i = N - 1; i >= 0; i--) {
      let x = +a[i] - br - +b[i];
      if (x < 0) { x += 2; br = 1; } else br = 0;
      res[i] = x; borrow[i] = br;
    }
    return { a, b, res, borrow, neg: br, N };
  }
  function drawSub() {
    const { a, b, res, borrow, neg, N } = subCalc();
    const shown = subPos;
    const d = (ch, cls) => '<span class="d' + (cls || '') + '">' + ch + '</span>';
    let h = '<div class="row"><span class="lbl">借り</span>';
    for (let i = 0; i < N; i++) {
      const from = i + 1;
      const show = (N - from) < shown && from < N && borrow[from] ? '1' : '';
      h += d(show, ' carry' + ((N - 1 - i) === shown - 1 ? ' hi' : ''));
    }
    h += '</div>';
    h += '<div class="row"><span class="lbl"></span>' + [...a].map((ch, i) => d(ch, (N - 1 - i) === shown - 1 ? ' hi' : '')).join('') + '</div>';
    h += '<div class="row"><span class="lbl">−</span>' + [...b].map((ch, i) => d(ch, (N - 1 - i) === shown - 1 ? ' hi' : '')).join('') + '</div>';
    h += '<div class="line"></div>';
    h += '<div class="row"><span class="lbl"></span>' + res.map((v, i) =>
      (N - 1 - i) < shown ? d(v, (N - 1 - i) === shown - 1 ? ' hi' : '') : d('_')).join('') + '</div>';
    $('subGrid').innerHTML = h;
    const n = $('subNote');
    if (shown === 0) {
      n.className = 'note info';
      n.innerHTML = '<strong>いちばん右の位</strong>から計算します。';
    } else if (shown <= N) {
      const i = N - shown;
      const bin = shown > 1 ? borrow[i + 1] : 0;
      const raw = +a[i] - bin - +b[i];
      n.className = 'note ' + (raw < 0 ? 'warn' : 'info');
      n.innerHTML = '右から ' + shown + ' 桁目：' + a[i] + (bin ? ' − 借り1' : '') + ' − ' + b[i] + ' ＝ ' +
        (raw < 0 ? '<strong>そのままでは引けないので上の位から1を借りて ' + (raw + 2) + '</strong>' : '<strong>' + raw + '</strong>');
    }
    if (shown >= N) {
      n.className = neg ? 'note ng' : 'note ok';
      n.innerHTML = neg
        ? '引く数のほうが大きいので、この桁数では正しく表せません（負の数になります）。5-4の補数を使えば計算できます。'
        : '計算が終わりました。答えは <strong>' + res.join('') + '(2)</strong>です。';
    }
    $('subCheck').innerHTML = dec(a) + ' − ' + dec(b) + ' ＝ ' + (dec(a) - dec(b)) + '　（2進法：' + res.join('') + '）';
  }

  /* ---------- STEP3 シフト ---------- */
  function drawShift() {
    const s = clean($('shiftIn').value, 8);
    const left = s.slice(1) + '0';
    const right = '0' + s.slice(0, 7);
    const row = (str, box, dropIdx) => {
      $(box).innerHTML = [...str].map((c, i) =>
        '<div class="b' + (c === '1' ? ' on' : '') + (dropIdx === i ? ' gone' : '') + '">' + c + '</div>').join('');
    };
    row(s, 'shiftOrig', -1);
    row(left, 'shiftLeft', -1);
    row(right, 'shiftRight', -1);
    const v = dec(s);
    const n = $('shiftNote');
    n.className = 'note ok';
    n.innerHTML = 'もとの数 <strong>' + v + '</strong>　→　2倍：<strong>' + dec(left) + '</strong>（' + left + '）' +
      '　→　半分：<strong>' + dec(right) + '</strong>（' + right + '）<br>' +
      (v * 2 > 255 ? '<span style="color:var(--ng)">2倍すると8ビットからあふれるため、左端の1が消えて正しい値になりません。</span>'
                   : 'ビットを1つずらすだけで2倍・半分になります。' + (v % 2 ? '（半分にすると小数部分が切り捨てられます）' : ''));
  }

  /* ---------- STEP4 ドリル ---------- */
  let dScore = 0, dTotal = 0, dAns = '';
  function newDrill() {
    const kind = Math.floor(Math.random() * 3);
    const a = Math.floor(Math.random() * 120) + 20, b = Math.floor(Math.random() * 100) + 5;
    let q, choices;
    if (kind === 0) {
      const s = a + b;
      dAns = s.toString(2).padStart(8, '0');
      q = a.toString(2).padStart(8, '0') + '(2) ＋ ' + b.toString(2).padStart(8, '0') + '(2) ＝ ？';
      choices = [dAns, (s + 1).toString(2).padStart(8, '0'), (a ^ b).toString(2).padStart(8, '0'), (s - 2).toString(2).padStart(8, '0')];
    } else if (kind === 1) {
      const x = Math.max(a, b), y = Math.min(a, b), s = x - y;
      dAns = s.toString(2).padStart(8, '0');
      q = x.toString(2).padStart(8, '0') + '(2) − ' + y.toString(2).padStart(8, '0') + '(2) ＝ ？';
      choices = [dAns, (s + 1).toString(2).padStart(8, '0'), (s - 1).toString(2).padStart(8, '0'), (x + y).toString(2).padStart(8, '0')];
    } else {
      const x = Math.floor(Math.random() * 100) + 5;
      dAns = (x * 2).toString(2).padStart(8, '0');
      q = x.toString(2).padStart(8, '0') + '(2) を2倍すると？';
      choices = [dAns, Math.floor(x / 2).toString(2).padStart(8, '0'), (x + 1).toString(2).padStart(8, '0'), (x * 2 + 1).toString(2).padStart(8, '0')];
    }
    $('dText').textContent = q;
    const box = $('dChoices'); box.className = 'choice4'; box.innerHTML = '';
    shuffle([...new Set(choices)]).forEach(c => {
      const b2 = document.createElement('button');
      b2.className = 'btn'; b2.textContent = c + '(2)'; b2.dataset.c = c; b2.style.textAlign = 'center';
      b2.addEventListener('click', () => answerDrill(c));
      box.appendChild(b2);
    });
    $('dFb').hidden = true;
    $('dProgress').textContent = (dTotal + 1) + ' 問目';
  }
  function answerDrill(c) {
    const ok = c === dAns, box = $('dChoices');
    box.classList.add('locked');
    [...box.children].forEach(b => {
      if (b.dataset.c === dAns) b.classList.add('correct');
      else if (b.dataset.c === c) b.classList.add('wrong');
    });
    dTotal++; if (ok) dScore++;
    $('dScore').textContent = dScore; $('dTotal').textContent = dTotal;
    const fb = $('dFb'); fb.hidden = false;
    fb.className = 'note ' + (ok ? 'ok' : 'ng');
    fb.innerHTML = (ok ? '正解です。' : '正解は <strong>' + dAns + '(2)</strong>。') +
      '10進法では <strong>' + dec(dAns) + '</strong> です。';
  }

  function init() {
    ['addA', 'addB'].forEach(i => $(i).addEventListener('input', () => { addPos = 0; drawAdd(); }));
    $('addStep').addEventListener('click', () => { addPos = Math.min(9, addPos + 1); drawAdd(); });
    $('addAll').addEventListener('click', () => { addPos = 9; drawAdd(); });
    $('addReset').addEventListener('click', () => { addPos = 0; drawAdd(); });
    ['subA', 'subB'].forEach(i => $(i).addEventListener('input', () => { subPos = 0; drawSub(); }));
    $('subStep').addEventListener('click', () => { subPos = Math.min(9, subPos + 1); drawSub(); });
    $('subAll').addEventListener('click', () => { subPos = 9; drawSub(); });
    $('subReset').addEventListener('click', () => { subPos = 0; drawSub(); });
    $('shiftIn').addEventListener('input', drawShift);
    $('dNext').addEventListener('click', newDrill);
    window.Terms.glossary($('glossBox'), ['2進法', '基数変換', '16進法', '補数', 'デジタル']);
    drawAdd(); drawSub(); drawShift(); newDrill();
    window.Terms.attach();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
