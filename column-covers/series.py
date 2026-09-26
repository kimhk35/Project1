"""AI Insight Column 시리즈별 고정 테마와 번호 규칙

시리즈 테마는 바꾸지 않는다 새 칼럼은 해당 시리즈의 테마를 그대로 쓰고 번호만 이어 간다
"""

SERIES = {
    # 본연재 〈에이전틱 사고 · 온톨로지〉 00 01 02 ... 두 자리 번호 미색 종이 + 청록
    'main': dict(
        theme=dict(bg='#F3EEE4', ink='#16181D', acc='#0F6E68', acc2='#C8553D', mute='#6B6A66', dark=False),
        cat='SERIES · AGENTIC THINKING',
        kicker='AI Insight Column',
        footer='〈에이전틱 사고 · 온톨로지〉',
        num=lambda n: f'{n:02d}',
        numlabel=lambda n: 'PROLOGUE' if n == 0 else f'제{n}회',
    ),
    # Spin-Off S1 S2 ... 먹색 바탕 + 주황
    'spinoff': dict(
        theme=dict(bg='#111317', ink='#F2EFE8', acc='#FF5A36', acc2='#FFB200', mute='#9A968E', dark=True),
        cat='SPIN-OFF',
        kicker='AI Insight Column Spin-Off',
        footer='AI Insight Column',
        num=lambda n: f'S{n}',
        numlabel=lambda n: f'Spin-Off {n}',
    ),
    # Policy Lens PL1 PL2 ... 크림 바탕 + 청색
    'policy': dict(
        theme=dict(bg='#ECE5D3', ink='#1A1A1A', acc='#2E5C8A', acc2='#C8553D', mute='#6F6A5E', dark=False),
        cat='POLICY LENS',
        kicker='AI Insight Column · Policy Lens',
        footer='AI Insight Column',
        num=lambda n: f'PL{n}',
        numlabel=lambda n: f'Policy Lens {n}',
    ),
}
