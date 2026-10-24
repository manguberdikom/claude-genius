---
type: feedback
---
# Parallel worktree agentiga git stash berilmaydi

Worktree lar bitta `.git` ni bo'lishadi: `refs/stash` repo bo'yicha umumiy. Bir nechta parallel agent
"`stash -u && merge dev && stash pop`" qilsa, birining `pop` i boshqasining stashini o'z daraxtiga tushiradi
(`stash@{0}` almashib qoladi). Bir hodisada uchta guruhdan biri begona WIP ni olib, o'zi bekor qilgan; ish
yo'qolmagan, lekin tekshirishga vaqt ketgan.

Qoida: guruh worktree sida asosni yangilash `git add -A && git commit -m wip`, keyin `git merge dev`,
keyin tuzatish commitlari; birlashtirishda squash. Stash qoldig'ini solishtirganda `stash -u` kuzatilmagan
fayllari `stash^3` da turadi, asosiy daraxt bilan solishtirsa yolg'on "farq" chiqadi.
