# FeelUOwn Discord Rich Presence
这是一个实现 Discord RPC Rich Precense 服务的 FeelUOwn 插件

### 关于 What are these
- [What is Discord](https://discordapp.com/)
- [What is Rich Precense](https://discordapp.com/rich-presence)
- [What is FeelUOwn](https://github.com/cosven/FeelUOwn)

### 食用攻略 Usage

#### Release Version

1. 安装并第一次运行 FeelUOwn, 初始化文件夹
2. 下载插件 [Release 版本](https://github.com/BruceZhang1993/feeluown-discordrpc-plugin/releases/tag/v0.0.1)

```shell
# Using wget
cd /tmp
wget https://github.com/BruceZhang1993/feeluown-discordrpc-plugin/archive/v0.0.1.tar.gz
tar zxvf v0.0.1.tar.gz
cp -r ./feeluown-discordrpc-plugin-0.0.1 $HOME/.FeelUOwn/plugins/feeluown-discordrpc-plugin
```

#### Git Version

1. 安装并第一次运行 FeelUOwn, 初始化文件夹
2. 打开 Linux 终端并 `cd $HOME/.FeelUOwn/plugins`
3. 安装插件 v2.x 分支开发版

```shell
git clone https://github.com/BruceZhang1993/feeluown-discordrpc-plugin.git feeluown_discordrpc
```

### 插件更新 Upgrade

#### Git Version  

```shell
cd $HOME/.FeelUOwn/plugins/feeluown_discordrpc
git pull origin master
```

### 特性 Features

- 实时显示当前播放歌曲信息（歌曲名/演唱者等）
- 显示当前曲目播放剩余时间及播放进度
- 更多信息显示和插件配置支持有待开发
- 与 Discord RPC 的简单自动重连机制

### 反馈 Feedback

- 与插件有关建议与反馈请发 Issue
- 与 FeelUOwn 本体有关建议与反馈请前往 [FeelUOwn Issue](https://github.com/cosven/FeelUOwn/issues)

### 开源协议 License

- FeelUOwn Discord Rich Presence Plugin: [MIT](https://github.com/BruceZhang1993/feeluown-discordrpc-plugin/blob/master/LICENSE)
- FeelUOwn: [GPL3](https://github.com/cosven/FeelUOwn/blob/master/LICENSE)
