const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', '2026-11-06-the-house-roster-maio-household.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function app(storage = new Map()) {
  const nodes = new Map();
  const element = () => ({innerHTML: '', dataset: {}, listeners: {}, classList: {toggle() {}},
    setAttribute() {}, addEventListener(name, handler) { this.listeners[name] = handler; }});
  const inputs = ['m1:mon', 'x1:_'].map(key => {
    const [id, day] = key.split(':');
    const row = element(); row.dataset.id = id;
    const input = element(); input.key = key; input.dataset.day = day === '_' ? undefined : day;
    input.closest = () => row; return input;
  });
  const context = vm.createContext({console, Date, confirm: () => true, window: {print() {}},
    localStorage: {getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value)},
    document: {getElementById(id) { if (!nodes.has(id)) nodes.set(id, element()); return nodes.get(id); },
      querySelectorAll: selector => selector === '.row .daytick input' ? inputs : [], querySelector: () => null}});
  vm.runInContext(script, context);
  return {storage, run: code => vm.runInContext(code, context),
    click: id => nodes.get(id).listeners.click(),
    tick(key) {const input = inputs.find(x => x.key === key); input.checked = true; input.listeners.change({target: input});},
    rendered: id => nodes.get(id).innerHTML};
}

test('weekly completion survives reload but stays in its occurrence week', () => {
  const a = app(); a.tick('m1:mon');
  assert.equal(a.run("isTick('m1:mon')"), true);
  const b = app(a.storage);
  assert.equal(b.run("isTick('m1:mon')"), true);
  b.click('nextWeek'); assert.equal(b.run("isTick('m1:mon')"), false);
  b.click('prevWeek'); assert.equal(b.run("isTick('m1:mon')"), true);
});
test('monthly completion expires in the next displayed month', () => {
  const a = app(); a.tick('x1:_'); a.run('state.weekOffset=5');
  assert.equal(a.run("isTick('x1:_')"), false);
});
test('away weeks never assign work to Ricardo', () => {
  const a = app(); a.click('rotB');
  assert.equal(a.run("TASKS.flatMap(t=>activeDays(t).map(d=>resolve(t,d))).filter(o=>o==='RIC'||o==='BOTH').length"), 0);
  assert.match(a.rendered('insight'), /cover/i);
});
test('child-specific mornings disappear without custody', () => {
  const a = app(); a.click('kidsOff');
  assert.equal(a.run("TASKS.filter(t=>['m1','m2','m3','m6'].includes(t.id)).flatMap(activeDays).length"), 0);
});
test('helper coverage is two visits and total household minutes are conserved', () => {
  const a = app(); const before = a.rendered('stats'); a.click('helperOn');
  assert.equal(a.run("TASKS.find(t=>t.id==='h1').d.filter(d=>resolve(TASKS.find(t=>t.id==='h1'),d)==='HELP').length"), 2);
  assert.equal(a.rendered('stats').match(/Chore hours[\s\S]*?<div class="v">(\d+)/)[1], before.match(/Chore hours[\s\S]*?<div class="v">(\d+)/)[1]);
});
test('monthly tasks respect the selected person and helper-off clears its filter', () => {
  const a = app(); a.run("state.filter='RIC';renderGroups()");
  assert.ok(!a.rendered('groups').includes('data-id="x3"'));
  assert.ok(a.rendered('groups').includes('data-id="x1"'));
  a.run("state.helper=true;state.filter='HELP'"); a.click('helperOff');
  assert.equal(a.run('state.filter'), 'ALL');
});
test('shared work has no hidden load bucket and all minutes are represented', () => {
  const a = app();
  assert.equal(a.run('weeklyMinutes().BOTH'), undefined);
  assert.equal(a.run('Object.values(weeklyMinutes()).reduce((s,p)=>s+p.chore+p.care,0)'),
    a.run('TASKS.reduce((s,t)=>s+(t.zero?0:activeDays(t).length*t.m),0)'));
});
test("Julie's protected window is duty-free in home and away scenarios", () => {
  const a = app();
  for (const rot of ['A','B']) {
    a.run(`state.rot=${JSON.stringify(rot)}`);
    assert.equal(a.run("TASKS.filter(t=>!t.care&&!t.zero&&t.time>='17:00'&&t.time<'20:00').flatMap(t=>activeDays(t).map(d=>resolve(t,d))).filter(o=>o==='JUL'||o==='BOTH').length"), 0);
  }
});
test('legacy ticks are retained in the original period without changing their recovery entry', () => {
  const original = JSON.stringify({'m1:mon': 1, 'x1:_': 1});
  const a = app(new Map([['maio-house-roster-v1', original]]));
  assert.equal(a.run("isTick('m1:mon')"), true);
  assert.equal(a.run("isTick('x1:_')"), true);
  a.run('state.weekOffset=1'); assert.equal(a.run("isTick('m1:mon')"), false);
  a.run('state.weekOffset=3'); assert.equal(a.run("isTick('x1:_')"), true);
  a.run('state.weekOffset=5'); assert.equal(a.run("isTick('x1:_')"), false);
  assert.equal(a.storage.get('maio-house-roster-v1'), original);
});
test('away-week cover remains visible when the children are also away', () => {
  const a = app(); a.click('kidsOff'); a.click('rotB');
  assert.match(a.rendered('insight'), /need cover/);
});
