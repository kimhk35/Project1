const fs = require('fs');
const base = 'c:/upstage';

// 데이터 파일 eval
const dataCode = fs.readFileSync(base + '/script_data.js', 'utf8');
const domainsCode = fs.readFileSync(base + '/script_domains.js', 'utf8');
eval(dataCode);
eval(domainsCode);

console.log('=== 데이터 검증 ===');
console.log(`FRAMEWORK: ${FRAMEWORK.length}개 항목`);
FRAMEWORK.forEach((f, i) => {
  console.log(`  ${i+1}. ${f.order} ${f.title} — 태그 ${f.tags.length}개`);
});

let totalSub = 0;
console.log(`\nDOMAINS: ${DOMAINS.length}개 영역`);
DOMAINS.forEach((d) => {
  const subCount = d[4].length;
  totalSub += subCount;
  console.log(`  ${d[0]} ${d[2]} — 하위 ${subCount}개`);
});
console.log(`총 하위 주제: ${totalSub}개`);

console.log(`\n참고문헌: 국제 ${INT_REFS.length}개 + 국내 ${DOM_REFS.length}개 = ${INT_REFS.length + DOM_REFS.length}개`);

// HTML data-count 검증
const html = fs.readFileSync(base + '/index.html', 'utf8');
const dc7 = (html.match(/data-count="7"/g) || []).length;
const dc26 = (html.match(/data-count="26"/g) || []).length;
const dc32 = (html.match(/data-count="32"/g) || []).length;

console.log('\n=== HTML data-count 검증 ===');
console.log(`대분류 영역 data-count="7": ${dc7}개 발견 → ${dc7 > 0 ? 'OK' : 'MISSING'} (실제 ${FRAMEWORK.length}개)`);
console.log(`중분류 주제 data-count="26": ${dc26}개 발견 → ${dc26 > 0 ? 'OK' : 'MISSING'} (실제 ${totalSub}개)`);
console.log(`주요 문헌 data-count="32": ${dc32}개 발견 → ${dc32 > 0 ? 'OK' : 'MISSING'} (실제 ${INT_REFS.length + DOM_REFS.length}개)`);

// 스크립트 로드 순서
const scripts = html.match(/<script src="([^"]+)"/g).map(s => s.match(/<script src="([^"]+)"/)[1]);
console.log('\n=== 스크립트 로드 순서 ===');
scripts.forEach((s, i) => console.log(`  ${i+1}. ${s}`));

// 버그 수정 검증
const renderCode = fs.readFileSync(base + '/script_render.js', 'utf8');
const utilCode = fs.readFileSync(base + '/script_util.js', 'utf8');
const svgFixed = renderCode.includes('N[a]') && renderCode.includes('N[b]');
const revealAdded = utilCode.includes('.reveal');
console.log('\n=== 버그 수정 검증 ===');
console.log(`SVG N[a]/N[b] 수정: ${svgFixed ? 'OK' : 'NOT FIXED'}`);
console.log(`스크롤 리빌 .reveal 클래스: ${revealAdded ? 'OK' : 'NOT FIXED'}`);

console.log('\n=== 최종 판정 ===');
const allOk = dc7 > 0 && dc26 > 0 && dc32 > 0 && svgFixed && revealAdded &&
  scripts.length === 4 && scripts[0] === 'script_data.js' && scripts[1] === 'script_domains.js' &&
  scripts[2] === 'script_render.js' && scripts[3] === 'script_util.js';
console.log(allOk ? '모든 검증 통과!' : '일부 검증 실패 — 상세 확인 필요');
