# UGQ 每日签到配置

这份仓库已配置为每天北京时间 09:00 执行（GitHub 调度可能延迟）。
每次运行主动使用账号密码登录，不依赖 ChatGPT 浏览器或上次运行的 Cookie。
本工作流只向 `https://ugq.ai` 执行登录、个人信息和签到请求。

## 只需配置一次密码

打开本仓库 **Settings → Secrets and variables → Actions → New repository secret**：

- Name：`UGQ_PASSWORD`
- Secret：UGQ 当前登录密码

默认登录账号为 `gaojunyang`；如需修改，另建 Secret `UGQ_USERNAME`。
密码只放在 GitHub Secrets，不放在代码、Issue、工作流手动输入或提交文件中。
无需设置 `NEWAPI_ACCOUNTS`、`CONFIG_URL` 或手动提取 Cookie，也无需启用 Pages。

## 首次运行

打开 **Actions**。若 Fork 的工作流尚未启用，先点击启用工作流的按钮。
选择 **UGQ 每日签到 → Run workflow → Run workflow**。
在运行详情的 **登录 UGQ 并签到** 步骤中确认：

1. 出现自动登录成功结果。
2. 出现签到成功或服务器明确返回当天已签到。
3. 最终汇总成功 1、失败 0。

仓库配置与模拟回归测试通过不等于网站签到已成功，仍需首次真实运行验证。
缺少密码、密码错误或网站要求额外验证时，运行会失败并留下错误结果。

## 可选通知

未配置通知渠道时，在 GitHub Actions 中查看运行记录；GitHub 的失败提醒取决于你自己的通知设置。
如需 Server酱，添加 Secret `SERVERCHAN_SENDKEY`。
如需邮件，按代码中实际使用的变量添加 `EMAIL_SMTP_HOST`、`EMAIL_SMTP_PORT`、`EMAIL_USER`、`EMAIL_PASS`、`EMAIL_TO`（可选 `EMAIL_FROM`）。

## 运行边界

本配置不报名抽奖、不充值、不购买、不修改 UGQ 账户设置。
原 ChatGPT 签到任务不会由本项目自动停用。新项目真实签到成功后，再停用旧任务，避免重复运行。
公共仓库的定时工作流可能因连续 60 天仓库无活动而被 GitHub 自动禁用；保留的 keepalive 工作流仅输出日志，不能保证避免此限制。
如需长期严格无人值守，可以把同样的登录与签到代码迁移到自己的常开服务器。
