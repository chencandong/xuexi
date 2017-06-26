#Git总结 
###git的常见语法
git init 创建版本库，该目录的所有文件都可以被git管理起来

git status 查看当前的仓库的状态

git diff filename 查看文件的变动情况 

git log 查看仓库变化的情况 

git reset --hard HEAD 回退到上一个版本

git reflog  用来记录每一次commit或者reset的命令

git add 把所有要提交的修改放到暂存区，然后执行git commit就可以一次性把所有的修改都提交到所在的分支

git checkout -- filename
