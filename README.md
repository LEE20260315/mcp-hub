<div align="center"><br><br>
<img src="https://raw.githubusercontent.com/LEE20260315/mcp-hub/main/docs/assets/banner-xicheng.jpg" alt="墨道具箱" width="720"/>
<br><br>

# 墨 道 具 箱
<sub>M C P &nbsp;·&nbsp; H U B</sub>
<br>

<sub>― 靜謐而文，案頭之器 ―</sub>

<sub>凡十二器，藏於一函；一令既出，諸具皆備。</sub>
<br>

![](https://img.shields.io/badge/license-MIT-141414?style=flat-square)
![](https://img.shields.io/badge/servers-12-141414?style=flat-square)
![](https://img.shields.io/badge/clients-5-141414?style=flat-square)
![](https://img.shields.io/github/stars/LEE20260315/mcp-hub?style=flat-square&color=9C2A2A&label=stars)

<br>

<sub><a href="#序">序</a> &nbsp;·&nbsp; <a href="#器">器</a> &nbsp;·&nbsp; <a href="#案">案</a> &nbsp;·&nbsp; <a href="#法">法</a> &nbsp;·&nbsp; <a href="#問">問</a></sub>

<br><br>

<img src="https://raw.githubusercontent.com/LEE20260315/mcp-hub/main/docs/assets/seal-xicheng.png" alt="西城閒人" width="72"/>

<br></div>

---

## 序 <a id="序"></a>

凡治學者，必有文房；凡馭 Agent 者，亦當備其器。

本函收 MCP 服務器十二，配通用 `mcp.json` 一卷、安裝腳本三紙，
俾 Trae、Claude Desktop、Cursor、VS Code、Windsurf 五客，
一令之間，文件可讀、終端可驅、網頁可閱、表簿可理、檢索可成。

<br>

## 器 <a id="器"></a>

<sub>※ 編號取漢字前導，以求案頭之整齊。</sub>

| 號 | 名 | 用 | 棲 |
|---|---|---|---|
| 〇一 | Filesystem          | 遍覽群籍，增刪改移，無遠弗屆     | Node |
| 〇二 | Desktop Commander   | 驅策終端，運籌帷幄，令行禁止     | Node |
| 〇三 | Sequential Thinking | 層層遞進，抽絲剝繭，洞若觀火     | Node |
| 〇四 | Memory              | 博聞強識，歷歷在目，溫故知新     | Node |
| 〇五 | context7            | 博覽群書，提要鉤玄，旁徵博引     | Node |
| 〇六 | Puppeteer           | 駕馭無頭，遊刃有餘，無形之刃     | Node |
| 〇七 | DuckDuckGo          | 隱姓埋名，搜奇索隱，無跡可尋     | uvx  |
| 〇八 | lark-mcp            | 飛書傳信，往來無礙，瞬息千里     | Node |
| 〇九 | Excel               | 縱橫表簿，條分縷析，井然有序     | Node |
| 一〇 | Chrome DevTools     | 洞察秋毫，診脈開方，藥到病除     | Node |
| 一一 | 發現報告            | 運筆成章，條陳利弊，擲地有聲     | uvx  |
| 一二 | Playwright          | 跨瀏覽器試，百戰不殆，穩如磐石   | Node |

<br>

## 案 <a id="案"></a>

| 客 | 几 | 函 |
|---|---|---|
| Trae IDE        | Windows     | `%APPDATA%\Trae CN\User\mcp.json` |
| Claude Desktop  | Win / macOS | `…\Claude\claude_desktop_config.json` |
| Cursor          | 通用         | `~/.cursor/mcp.json` |
| VS Code (Cline) | 通用         | `…/globalStorage/.../mcp_settings.json` |
| Windsurf        | 通用         | `~/.windsurf/mcp.json` |

<br>

## 法 <a id="法"></a>

```bash
# macOS / Linux —— 一令而成
curl -fsSL https://raw.githubusercontent.com/LEE20260315/mcp-hub/main/install.sh | bash
```

```powershell
# Windows —— 同此一令
iwr -useb https://raw.githubusercontent.com/LEE20260315/mcp-hub/main/install.ps1 | iex
```

<sub>※ 凡首次運行，npm 與 uvx 皆需取依賴，稍候即成。</sub>

<br>

### 環境變量

```ini
LARK_APP_ID=xxxxxxxx
LARK_APP_SECRET=xxxxxxxx
```

<sub>※ `.env` 已入 `.gitignore`，密鑰不可付梓。</sub>

<br>

### 前置依賴

| 依 | 所需之器 | 取之之法 |
|---|---|---|
| Node.js ≥ 18 | Filesystem · Commander · Thinking · Memory · Puppeteer · Lark · Excel · Chrome · Playwright |  |
| Python + uv  | DuckDuckGo · 發現報告 | `pip install uv` |
| Chrome       | Puppeteer · Chrome DevTools |  |

<br>

### 自訂

凡欲改 Filesystem 所許之徑，編 `mcp.json` 中 Filesystem 之 `args` 即可。

欲廢一器，刪 `mcp.json` 中其條目。

欲添新器，於 `mcp.json` 之 `mcpServers` 下新增一節。

<br>

## 問 <a id="問"></a>

<details>
<summary>npx 不啟，何故？</summary>
<br>
請驗 Node.js ≥ 18 是否在席。首啟之時，須取依賴，候之即可。
</details>

<details>
<summary>uvx 之令不存？</summary>
<br>
執 <code>pip install uv</code>，並使 Python Scripts 入於 PATH。
</details>

<details>
<summary>飛書 lark 何以配？</summary>
<br>
往 <a href="">飛書開放平台</a> 立應用一所，取 App ID 與 App Secret 二鑰，書於 <code>.env</code>。
</details>

<details>
<summary>Puppeteer 或 Playwright 須另裝瀏覽器否？</summary>
<br>
首次運行時自取 Chrome / Chromium，無需手動。
</details>

<br>

---

<div align="center">
<img src="https://raw.githubusercontent.com/LEE20260315/mcp-hub/main/docs/assets/seal-xicheng.png" alt="西城閒人" width="64"/>
<br>
<sub>紙承墨，墨載意，意馭器</sub><br>
<sub>纸承墨，墨载意，意驭器 · Paper receives ink, ink carries meaning, meaning commands the instrument</sub><br>
<sub>西城閒人 · 識</sub><br>
<sub>MIT © 2026 ・ LEE20260315</sub>
</div>
