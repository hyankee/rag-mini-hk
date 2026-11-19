"""A dependency-free single-page demo UI."""


INDEX_HTML = r"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>RAG Mini HK</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #667085;
      --line: #e4e7ec;
      --accent: #2457d6;
      --accent-soft: #eaf0ff;
      --warn: #9a5b00;
      --warn-soft: #fff6e5;
      --ok: #087443;
      --ok-soft: #e9f7ef;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: radial-gradient(circle at 10% 0%, #e8efff 0, transparent 36%), var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang HK", "Noto Sans CJK SC", sans-serif;
      line-height: 1.55;
    }
    main { width: min(980px, calc(100% - 32px)); margin: 0 auto; padding: 44px 0 56px; }
    header { margin-bottom: 22px; }
    .eyebrow { color: var(--accent); font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    h1 { margin: 6px 0 8px; font-size: clamp(30px, 5vw, 48px); letter-spacing: -.03em; }
    .subtitle { margin: 0; color: var(--muted); max-width: 720px; }
    .status { display: inline-flex; gap: 8px; align-items: center; margin-top: 14px; padding: 6px 10px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel); color: var(--muted); font-size: 13px; }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--ok); }
    .dot.pending { background: var(--warn); }
    .card { background: var(--panel); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 12px 32px rgba(23, 32, 51, .06); }
    .ask-card { padding: 20px; }
    textarea { width: 100%; min-height: 96px; resize: vertical; border: 1px solid var(--line); border-radius: 12px; padding: 13px 14px; font: inherit; color: var(--ink); outline: none; }
    textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
    .row { display: flex; gap: 10px; align-items: center; justify-content: space-between; margin-top: 12px; flex-wrap: wrap; }
    button { border: 0; border-radius: 10px; padding: 10px 16px; font: inherit; font-weight: 700; cursor: pointer; background: var(--accent); color: white; }
    button:disabled { opacity: .55; cursor: wait; }
    .examples { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
    .example { background: #f8f9fc; color: var(--ink); border: 1px solid var(--line); font-weight: 500; padding: 7px 10px; font-size: 13px; }
    .example:hover { border-color: var(--accent); color: var(--accent); }
    .hint { color: var(--muted); font-size: 12px; }
    .result { margin-top: 18px; padding: 20px; display: none; }
    .result.visible { display: block; }
    .badge { display: inline-block; padding: 4px 9px; border-radius: 999px; font-size: 12px; font-weight: 700; background: var(--accent-soft); color: var(--accent); }
    .badge.warn { background: var(--warn-soft); color: var(--warn); }
    .answer { white-space: pre-wrap; margin: 12px 0 0; font-size: 16px; }
    .notice { margin-top: 10px; padding: 10px 12px; border-radius: 10px; background: var(--warn-soft); color: var(--warn); font-size: 13px; }
    .sources { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-top: 16px; }
    .source { border: 1px solid var(--line); border-radius: 12px; padding: 12px; background: #fbfcff; }
    .source-top { display: flex; justify-content: space-between; gap: 8px; color: var(--muted); font-size: 12px; }
    .source-id { color: var(--accent); font-weight: 800; }
    .source h3 { margin: 7px 0 5px; font-size: 14px; }
    .source p { margin: 0; color: var(--muted); font-size: 13px; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
    .error { margin-top: 12px; padding: 12px; border-radius: 10px; background: #fff0f0; color: #b42318; white-space: pre-wrap; }
    footer { margin-top: 18px; color: var(--muted); font-size: 12px; }
    code { background: #f2f4f7; padding: 1px 5px; border-radius: 5px; }
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">Portfolio demo · Retrieval-Augmented Generation</div>
      <h1>RAG Mini HK</h1>
      <p class="subtitle">面向香港行业资料的引用式问答。检索 8 份合成行业简报，返回带 <code>[S1]</code> 来源的答案；证据不足时说“资料中无法确认”。</p>
      <div class="status"><span class="dot pending" id="status-dot"></span><span id="status-text">正在检查索引…</span></div>
    </header>

    <section class="card ask-card">
      <textarea id="question" placeholder="例如：物流行业哪些单证适合做结构化抽取？"></textarea>
      <div class="row">
        <span class="hint">Cmd/Ctrl + Enter 提交 · 检索层固定 top-3</span>
        <button id="ask-button" type="button">提问</button>
      </div>
      <div class="examples">
        <button class="example" data-q="物流行业哪些单证适合做结构化抽取？">物流单证抽取</button>
        <button class="example" data-q="医疗行业使用 LLM 时，为什么不能把病人资料随意外发？">医疗隐私边界</button>
        <button class="example" data-q="香港 2026 年 LLM 工程师的平均月薪是多少？">无答案拒答</button>
        <button class="example" data-q="香港金融科技行业常见的三类岗位是什么？">岗位画像</button>
      </div>
    </section>

    <section class="card result" id="result">
      <div id="mode-badge" class="badge">生成回答</div>
      <div id="notice" class="notice" style="display:none"></div>
      <div id="answer" class="answer"></div>
      <div id="sources" class="sources"></div>
    </section>
    <div id="error" class="error" style="display:none"></div>
    <footer>仅用于学习与作品展示；行业内容是合成整理，不是官方原文或实时招聘信息。</footer>
  </main>

  <script>
    const questionEl = document.getElementById("question");
    const askButton = document.getElementById("ask-button");
    const resultEl = document.getElementById("result");
    const answerEl = document.getElementById("answer");
    const sourcesEl = document.getElementById("sources");
    const modeBadge = document.getElementById("mode-badge");
    const noticeEl = document.getElementById("notice");
    const errorEl = document.getElementById("error");
    const statusText = document.getElementById("status-text");
    const statusDot = document.getElementById("status-dot");

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
      }[ch]));
    }

    async function loadHealth() {
      try {
        const res = await fetch("/api/health");
        const data = await res.json();
        statusDot.classList.remove("pending");
        statusText.textContent = data.status === "ready"
          ? `${data.chunks} chunks · ${data.llm_mode} · ${data.embed_model}`
          : "索引为空，请先运行 build_index.py";
      } catch (err) {
        statusText.textContent = "无法连接 API";
      }
    }

    async function ask() {
      const question = questionEl.value.trim();
      if (question.length < 2) return;
      askButton.disabled = true;
      errorEl.style.display = "none";
      try {
        const res = await fetch("/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question, top_k: 3 }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "请求失败");
        resultEl.classList.add("visible");
        modeBadge.textContent = data.mode === "generated" ? "生成回答" : "仅检索证据";
        modeBadge.className = "badge" + (data.mode === "generated" ? "" : " warn");
        noticeEl.style.display = data.mode === "generated" ? "none" : "block";
        noticeEl.textContent = data.mode === "generated" ? "" : "未调用生成模型；以下是检索层找到的证据。配置 DEEPSEEK_API_KEY 后可生成带引用的答案。";
        answerEl.textContent = data.answer;
        sourcesEl.innerHTML = (data.sources || []).map((s) => `
          <article class="source">
            <div class="source-top"><span class="source-id">[S${s.rank}]</span><span>cosine ${Number(s.score).toFixed(3)}</span></div>
            <h3>${escapeHtml(s.section)}</h3>
            <div class="source-top"><span>${escapeHtml(s.doc_id)}</span><span>v${escapeHtml(s.version)}</span></div>
            <p>${escapeHtml(s.text.slice(0, 180))}…</p>
          </article>`).join("");
      } catch (err) {
        errorEl.style.display = "block";
        errorEl.textContent = String(err.message || err);
      } finally {
        askButton.disabled = false;
      }
    }

    askButton.addEventListener("click", ask);
    questionEl.addEventListener("keydown", (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") ask();
    });
    document.querySelectorAll(".example").forEach((button) => {
      button.addEventListener("click", () => { questionEl.value = button.dataset.q; questionEl.focus(); });
    });
    loadHealth();
  </script>
</body>
</html>
"""

