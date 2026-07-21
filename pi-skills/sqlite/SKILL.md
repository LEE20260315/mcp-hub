---
name: sqlite
description: 操作 SQLite 数据库。当用户要建库、建表、查询、插入、更新、分析本地数据、量化回测数据存储时使用。支持 sqlite3 CLI 和 Node.js 脚本两种方式。
---

# SQLite 数据库

## 两种使用方式

### 方式一：sqlite3 CLI（推荐简单查询）

先确认已安装：

```bash
sqlite3 -version || echo "未安装，可用: winget install SQLite.SQLite"
```

基本操作：

```bash
# 创建/打开数据库
sqlite3 "C:/path/to/data.db"

# 直接执行 SQL（不进交互）
sqlite3 "C:/path/to/data.db" "SELECT * FROM trades LIMIT 10;"

# 导出为 CSV
sqlite3 -header -csv "C:/path/to/data.db" "SELECT * FROM trades" > trades.csv

# 执行脚本文件
sqlite3 "C:/path/to/data.db" < schema.sql
```

### 方式二：Node.js 脚本（推荐程序化操作）

`better-sqlite3` 是同步 API，最简单：

```bash
# 一次性安装
npm install better-sqlite3
```

示例脚本 `query.js`：

```javascript
const Database = require('better-sqlite3');
const db = new Database('C:/path/to/data.db');

// 建表
db.exec(`CREATE TABLE IF NOT EXISTS trades (
  id INTEGER PRIMARY KEY,
  symbol TEXT,
  side TEXT,
  price REAL,
  qty REAL,
  ts TEXT DEFAULT (datetime('now'))
)`);

// 插入（参数化防注入）
const insert = db.prepare('INSERT INTO trades (symbol, side, price, qty) VALUES (?, ?, ?, ?)');
insert.run('RB2510', 'buy', 3520.5, 2);

// 查询
const rows = db.prepare('SELECT * FROM trades WHERE symbol = ? ORDER BY ts DESC LIMIT 10').all('RB2510');
console.log(rows);

db.close();
```

运行：`node query.js`

## 量化场景常用模式

### 存储行情/交易数据

```sql
CREATE TABLE klines (
  ts INTEGER,           -- 时间戳
  symbol TEXT,
  open REAL, high REAL, low REAL, close REAL,
  volume REAL
);
CREATE INDEX idx_klines_symbol_ts ON klines(symbol, ts);
```

### 批量插入提速

```javascript
const insertMany = db.transaction((rows) => {
  for (const r of rows) insert.run(...r);
});
insertMany(bigArray);
```

## 注意事项

- 数据库文件路径用引号包裹，含中文/空格时尤其重要
- 量化大数据量建议加索引 + WAL 模式：`PRAGMA journal_mode=WAL;`
- 临时分析完可删 `.db` 文件，不影响其他
