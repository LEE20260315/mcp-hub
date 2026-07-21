---
name: time
description: 时间与时区工具。当用户要查当前时间、做时区转换、日期计算、定时任务排程、跨时区对照时使用。基于系统 date 命令和 Node.js Date 对象。
---

# 时间与时区

## 当前时间

```bash
# 本地时间（Asia/Shanghai）
date "+%Y-%m-%d %H:%M:%S %Z"

# UTC 时间
date -u "+%Y-%m-%d %H:%M:%S UTC"

# Unix 时间戳
date +%s

# 星期几
date "+%A"
```

## 时区转换

```bash
# 查某时区当前时间（需 tzdata）
TZ="America/New_York" date "+%Y-%m-%d %H:%M:%S %Z"
TZ="Europe/London" date "+%Y-%m-%d %H:%M:%S %Z"
TZ="Asia/Tokyo" date "+%Y-%m-%d %H:%M:%S %Z"
```

## 日期计算

```bash
# 明天/后天
date -d "+1 day" "+%Y-%m-%d"
date -d "+7 days" "+%Y-%m-%d"

# 3 天前
date -d "-3 days" "+%Y-%m-%d"

# 两个日期相差天数
echo $(( ($(date -d "2026-12-31" +%s) - $(date -d "2026-07-21" +%s)) / 86400 ))
```

## Node.js 方式（跨平台更稳）

Windows 的 `date` 命令和 Linux 不同，复杂计算建议用 Node.js：

```bash
node -e "
const now = new Date();
console.log('本地:', now.toLocaleString('zh-CN', {timeZone:'Asia/Shanghai'}));
console.log('纽约:', now.toLocaleString('en-US', {timeZone:'America/New_York'}));
console.log('伦敦:', now.toLocaleString('en-GB', {timeZone:'Europe/London'}));
console.log('东京:', now.toLocaleString('ja-JP', {timeZone:'Asia/Tokyo'}));
"
```

日期计算：

```bash
node -e "
const d = new Date('2026-07-21');
d.setDate(d.getDate() + 30);
console.log(d.toISOString().slice(0,10));
"
```

## 常用时区代码

| 时区 | TZ 值 |
|---|---|
| 北京 | Asia/Shanghai |
| 东京 | Asia/Tokyo |
| 纽约 | America/New_York |
| 伦敦 | Europe/London |
| 芝加哥 | America/Chicago |
| 新加坡 | Asia/Singapore |

## 期货交易常用

- 国内期货（上期所/大商所/郑商所）：Asia/Shanghai，日盘 09:00-15:00
- CME/ICE 等外盘：America/New_York 或 Europe/London
- 跨市场时差换算直接用上面的 node 一行命令
