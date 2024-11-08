# 怎么上传Stamon包？

### 须知

本站的Github仓库位于[https://github.com/stamon-rsc/stamon-rsc.github.io/](https://github.com/stamon-rsc/stamon-rsc.github.io/)

你可以通过提交PR的方式来申请上传Stamon包，仓库管理员会定期审核、批复、通过。

### 配置

先在当前目录（即``packages``目录）下填写``manifesto.json``，你需要在json的“``packages``”项里填写你的包的名字（包管理器在下载包时将会使用这个名字），并在你填写的项中再说明你的包对应的目录。

接着在包对应的目录当中编写相关的代码；请确保目录中至少有``information.json``和``README.md``（我们强烈建议添加LICENSE，以避免引起不必要的纠纷）

其中，``README.md``应尽量精简的讲述包的用法以及注意事项。

``information.json``至少需要填写以下项：

* "name": 这个包的具体名字（包管理器在下载包时并不会参考这个名字）
* "version": 这个包的版本（版本号的格式必须是**X.Y.Z**）
* "author": 这个包的作者
* "author-email": 作者的联系邮箱
* "short-description": 这个包的简短介绍
* "url": 有关这个包的网址
* "download-list": 下载这个包需要下载哪些文件（information.json会被自动下载，无需指定）

举个例子，现在有一个``enum``包，那么应该这样配置：

* 一个讲述了用法的``README.md``
* ``enum.st``
* 一个LICENSE
* information.json

```json
{
    "name": "Stamon-Enum",
    "version": "0.0.1",
    "author": "CLimber-Rong",
    "author-email": "woshiquxiangrong@outlook.com",
    "short-description": "a tiny package of enum",
    "url": "CLimber-Rong.github.io",
    "download-list": ["enum.st", "README.md", "LICENSE"]
}
```

* 在``manifesto.json``里的``packages``项中填写：

```json
"enum": {
    "dir-name":"enum"
}
```

### 敬告

1. 任何人都没有资格随意干涉别人的包
2. 如果包有更新，可以重新提交PR
3. 无论是PR还是issue，都应该说明具体目的
4. 仓库管理员不对任何包负责，任何与包有关的问题都应该去找对应的开发者

以上，谢谢！