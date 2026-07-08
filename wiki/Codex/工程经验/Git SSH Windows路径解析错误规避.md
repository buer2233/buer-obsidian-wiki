# Git SSH Windows路径解析错误规避

来源：.raw/Codex/工程经验/
日期：2026-07-03

---

## 背景

在 `D:\AI\Hermes\learn` 推送 GitHub 仓库时，普通 SSH 测试可以成功：

```text
ssh -T git@github.com
Hi buer2233! You've successfully authenticated, but GitHub does not provide shell access.
```

但直接执行 `git push` 时仍然报错：

```text
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

随后尝试用 `GIT_SSH_COMMAND` 强制 Git 使用 Windows OpenSSH 和指定私钥，第一次写法使用了 Windows 反斜杠路径：

```powershell
$env:GIT_SSH_COMMAND = 'C:\Windows\System32\OpenSSH\ssh.exe -i C:\Users\admin\.ssh\id_ed25519 -o IdentitiesOnly=yes'
git push -u origin master
```

Git 执行时报错：

```text
C:\Windows\System32\OpenSSH\ssh.exe -i C:\Users\admin\.ssh\id_ed25519 -o IdentitiesOnly=yes: C:WindowsSystem32OpenSSHssh.exe: command not found
fatal: Could not read from remote repository.
```

---

## 具体原因

`GIT_SSH_COMMAND` 不是单纯由 PowerShell 原生解析后执行，而是会被 Git for Windows / MSYS 运行时转交给 Git 内部的 SSH 调用链解析。

在这个解析链里，Windows 路径中的反斜杠 `\` 容易被当成转义字符，而不是稳定地当作路径分隔符。

因此：

```text
C:\Windows\System32\OpenSSH\ssh.exe
```

可能被解析成：

```text
C:WindowsSystem32OpenSSHssh.exe
```

路径分隔符丢失后，Git 找不到 SSH 可执行文件，于是报 `command not found`。

---

## 正确做法

在传给 Git、SSH、Git Bash、MSYS 等跨平台工具链的路径中，优先使用正斜杠：

```powershell
$env:GIT_SSH_COMMAND = 'C:/Windows/System32/OpenSSH/ssh.exe -i C:/Users/admin/.ssh/id_ed25519 -o IdentitiesOnly=yes'
git push -u origin master
```

本次使用该写法后推送成功：

```text
Branch 'master' set up to track remote branch 'master' from 'origin'.
To github.com:buer2233/learn-everyday-loop.git
 * [new branch]      master -> master
```

---

## 以后避免规则

1. PowerShell 中调用 Windows 原生命令时，反斜杠路径通常没问题。
2. 只要路径会进入 Git、SSH、Git Bash、MSYS、Node、Python CLI 等跨平台解析链，优先写成 `C:/xxx/yyy`。
3. 设置 `GIT_SSH_COMMAND` 时，不要使用反斜杠路径，统一使用正斜杠路径。
4. 如果 `ssh -T git@github.com` 成功但 `git push` 失败，优先检查 Git 使用的 SSH 客户端、私钥、ssh-agent 是否和当前 shell 一致。
5. 更稳定的长期方案是配置 `~/.ssh/config`，用 Host alias 固定私钥，减少每次手写 `GIT_SSH_COMMAND`。

---

## 可复用命令

```powershell
$env:GIT_SSH_COMMAND = 'C:/Windows/System32/OpenSSH/ssh.exe -i C:/Users/admin/.ssh/id_ed25519 -o IdentitiesOnly=yes'
git push
```

---

## 可选长期配置

在 `C:\Users\admin\.ssh\config` 中配置：

```sshconfig
Host github.com
    HostName github.com
    User git
    IdentityFile C:/Users/admin/.ssh/id_ed25519
    IdentitiesOnly yes
```

之后可以正常使用：

```powershell
git push
```

---

## 🔗 关联文档

- [[Docker]] — Docker使用经验
- [[Jenkins全攻略]] — Jenkins配置经验

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[Docker]] — AI测试主题关联
- [[Jenkins全攻略]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[安卓移动端appium环境搭建流程]] — AI测试主题关联
- [[SKILL发布L站的说明]] — AI测试主题关联
- [[常用SKILL总结]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[接口安全测试]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
