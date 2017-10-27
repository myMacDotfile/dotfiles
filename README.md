# Lzw does dotfiles

這份 dotfiles 是 fork 自 [Holman's dotfiles](https://github.com/holman/dotfiles)，並根據個人的需求修改。

閱讀完這份文件之後，如果有興趣，歡迎 fork 一份回去配置成適合自己的 dotfiles。

更多的 dotfiles 請參考 [GitHub does dotfiles](https://dotfiles.github.io/)。

# Quick Start

## Erase and reinstall OS X

如果你打算從乾淨的 Mac 環境開始，請參閱「[OS X：如何清除並安裝](http://support.apple.com/zh-tw/HT5943)」。

## Install Xcode

1. 更新 App Store。
2. 安裝 [Xcode](https://itunes.apple.com/us/app/xcode/id497799835?mt=12)。
3. 開啟 Terminal，安裝 Xcode Command Line Tools:

```bash
$ xcode-select --install
```

## Install dotfiles

[下載](https://github.com/amowu/dotfiles/archive/master.zip)或使用 git clone 一份到 `$HOME` 目錄底下的 `.dotfiles` 資料夾裡面:

```bash
$ git clone https://github.com/amowu/dotfiles.git ~/.dotfiles
```

進入 `.dotfiles` 資料夾:

```bash
$ cd ~/.dotfiles
```

安裝 dotfiles:

```bash
$ ./script/bootstrap
```

`bootstrap.sh` 這個程式會自動完成以下工作:

1. 檢查並安裝 [Homebrew](http://brew.sh/)。
2. 檢查並安裝 [Oh My Zsh](http://ohmyz.sh/)。
3. 檢查並連結 dotfiles (.zshrc, .vimrc, .gitconfig, .gitignore, ...)。
4. 設置 Mac OS X 的 defaults settings。
5. 更新並安裝 Homebrew packages (binaries, fonts, apps)。

完成之後，手動安裝一些 App Store 上才有的軟體 (Dash, Moom, ...)。

## Restore backup

使用 [Mackup](https://github.com/lra/mackup) 進行備份回復:

```bash
$ mackup restore
```

什麼是 Mackup? 底下介紹。

# How To Use

## dotfiles

執行 `~/.dotfiles/script/bootstrap` 的時候，腳本會將目錄底下所有的 `*.symlink` 檔案透過 `ln` 命令建立連結至 `$HOME` 目錄底下:

| topic  | *.symlink          | .dotfiles     |
| ------ | ------------------ | ------------- |
| git    | gitconfig.symlink  | ~/.gitconfig  |
|        | gitignore.symlink  | ~/.gitignore  |
| mackup | mackup.cfg.symlink | ~/.mackup.cfg |
| vim    | vimrc.symlink      | ~/.vimrc      |
| zsh    | zshrc.symlink      | ~/.zshrc      |

### Topical

每一個環境的配置是以資料夾的形式被獨立區分。例如，如果想要新增 "Java" 的配置到 dotfiles，你可以簡單的新增一個命名為 `java` 的資料夾，然後將檔案建至目錄底下。

- 任何副檔名是 `.zsh` 的檔案將在 shell 執行時被自動載入至環境中。
- 任何副檔名是 `.symlink` 的檔案將在你執行 `script/bootstrap` 安裝時被連結至 `$HOME` 目錄底下。.

### Components

一些目錄中比較特別的檔案:

- **bin/**: 任何在 `bin/` 目錄底下的檔案可以在 shell 執行時直接使用。
- **topic/*.zsh**: 任何 `.zsh` 結尾的檔案都會在 shell 執行時被載入至環境。
- **topic/path.zsh**: 任何命名為 `path.zsh` 的檔案會在 shell 執行時優先被載入至 `$PATH`。
- **topic/*.symlink**: 任何 `*.symlink` 結尾的檔案都會在 `$HOME` 目錄底下建立連結。這可以讓你在配置環境的時候也保持版本控制的優點。新增 symlink 的時候需要執行 `script/bootstrap` 安裝。

不同於 [Holman's dotfiles](https://github.com/holman/dotfiles)，我修改了一些部分:

- Shell 的部分改用 [Oh My Zsh](http://ohmyz.sh/) 取代原作者自己配置的 zsh。
- 移除 **topic/aliases.zsh**、**topic/completion.zsh** 等檔案，改用 Oh My Zsh 的 [plugins]。(https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins) 代替。
- 移除 **zsh/prompt.zsh**、**zsh/window.zsh.zsh** 等檔案，改用 Oh My Zsh 的 [themes]。(https://github.com/robbyrussell/oh-my-zsh/wiki/Themes) 代替。
- dotfiles 只專注在 **topic/*.symlink**、**topic/path.zsh** 的配置。

## OS X

`bin/dot` 是一支簡單的腳本，會在 `script/bootstrap` 配置完 dotfiles 之後執行，安裝自定的 OS X 程式並設定系統參數配置。

執行 `$ dot` 之後，它會跑以下兩支腳本檔:

1. `$HOME/.dotfiles/osx/set-defaults.sh` - OS X defaults setting
2. `$HOME/.dotfiles/Brewfile` - Homebrew packages
3. 任何目錄下檔名是 `install.sh` 的檔案將被執行。

### Homebrew packages

執行 `$ dot` 的時候，腳本會根據 `Brewfile` 使用 [Homebrew](http://brew.sh/) 和 [Homebrew Cask](http://caskroom.io/) 來安裝 **binary**、**font** 還有 **app**，可以依照個人需求修改這個檔案，增加或減少自己需要的 packages:

```
brew 'git'
brew 'tree'
brew ...
```

應用程式可以用 `$ brew cask search XXX` 或是 [Cask Search](http://caskroom.io/search) 網站搜尋是否存在。

```bash
cask 'dropbox'
cask 'google-chrome'
cask ...
```

字型都是以 **font-XXX** 的形式命名，可以用 `$ brew cask search /font-XXX/` 搜尋是否存在。

```
cask 'font-roboto'
cask ...
```

以下是我目前安裝的 packages：

#### Binaries

| name | 說明 |
| --- | --- |
| [ffmpeg](https://www.ffmpeg.org/) | A complete, cross-platform solution to record, convert and stream audio and video. |
| [git-flow](https://github.com/nvie/gitflow) | Git extensions to provide high-level repository operations for Vincent Driessen's branching model |
| [gnupg](https://www.gnupg.org/index.html) | GnuPG is a complete and free implementation of the OpenPGP standard as defined by RFC4880 (also known as PGP) |
| [gnupg2](https://www.gnupg.org/index.html) | |
| [go](https://golang.org/) | The Google's Go Programming Language |
| [grc](http://kassiopeia.juls.savba.sk/~garabik/software/grc.html) | Generic Colouriser is yet another colouriser for beautifying your logfiles or output of commands |
| [httpie](https://github.com/jkbrzt/httpie) | HTTPie (pronounced aych-tee-tee-pie) is a command line HTTP client. |
| [irssi](http://irssi.org/) | The client of the future |
| [mackup](https://github.com/lra/mackup) | Keep your application settings in sync |
| [mongodb](https://www.mongodb.org/) | MongoDB is the next-generation database that lets you create applications never before possible. |
| [nvm](https://github.com/creationix/nvm) | Node Version Manager |
| [opencc](https://github.com/BYVoid/OpenCC) | A project for conversion between Traditional and Simplified Chinese |
| [pyenv](https://github.com/yyuu/pyenv) | Simple Python version management |
| [rethinkdb](https://www.rethinkdb.com/) | the open-source database for the realtime web |
| [ssh-copy-id](http://linux.die.net/man/1/ssh-copy-id) | ssh-copy-id is a script that uses ssh to log into a remote machine |
| [terraform](https://www.terraform.io/) | Terraform is a tool for building, changing, and combining infrastructure safely and efficiently. |
| [trash](http://hasseg.org/trash/) | This is a small command-line program for OS X that moves files or folders to the trash |
| [tree](http://mama.indstate.edu/users/ice/tree/) | Tree is a recursive directory listing command that produces a depth indented listing of files |
| [unrar](http://www.rarlab.com) | Extract, view, and test RAR archives |
| [youtube-dl](https://github.com/rg3/youtube-dl/) | Small command-line program to download videos from YouTube.com and other video sites |

#### Fonts

| name | 說明 |
| --- | --- |
| [font-hack](http://sourcefoundry.org/hack/) | A typeface designed for source code |
| [font-noto-sans](https://www.google.com/get/noto/help/cjk/) | Noto Sans CJK |
| [font-roboto](http://www.google.com/fonts/specimen/Roboto) | Roboto |
| [font-source-code-pro](http://www.google.com/fonts/specimen/Source+Code+Pro) | Source Code Pro |

#### Apps

| name | 說明 |
| --- | --- |
| [alfred](http://www.alfredapp.com/) | Alfred is an award-winning productivity application for Mac OS X |
| [atom](https://atom.io/) | Atom is a text editor that's modern, approachable, yet hackable to the core |
| [beyond-compare](http://www.scootersoftware.com/) | Scooter software's Beyond Compare is a Windows utility that combines directory compare and file compare functions in one package. |
| [charles](http://www.charlesproxy.com/) | Charles is an HTTP proxy / monitor / Reverse Proxy that enables a developer to view all of the HTTP and SSL / HTTPS traffic between their machine and the Internet. |
| [cleanmymac](http://macpaw.com/cleanmymac) | Clean, optimize, and maintain your Mac with the all-new CleanMyMac 3. |
| [dockertoolbox](https://www.docker.com/toolbox) | The Docker Toolbox is an installer to quickly and easily install and setup a Docker environment on your computer. |
| [dropbox](http://www.dropbox.com/) | Dropbox is a service that keeps your files safe, synced, and easy to share |
| [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) | The only browser made for developers like you. |
| [flux](https://justgetflux.com/) | f.lux makes your computer screen look like the room you're in, all the time. |
| [gitter](https://gitter.im/apps) | Gitter is built on top of GitHub and is tightly integrated with your organisations, repositories, issues and activity. |
| [google-chrome](www.google.com/chrome) | Google Chrome is a browser that combines a minimal design with sophisticated technology to make the web faster, safer, and easier. |
| [heroku-toolbelt](https://toolbelt.heroku.com/) | Heroku command-line tooling for working with the Heroku platform, on OS X, Windows and Debian/Ubuntu. |
| [istat-munus](https://bjango.com/mac/istatmenus/) | An advanced Mac system monitor for your menubar |
| [iterm2](http://iterm2.com/) | iTerm2 is a terminal emulator for Mac OS X that does amazing things. |
| [keka](http://www.kekaosx.com/) | the free Mac OS X file archiver |
| [neteasemusic](http://music.163.com/) | 网易云音乐是一款专注于发现与分享的音乐产品，依托专业音乐人、DJ、好友推荐及社交功能，为用户打造全新的音乐生活。 |
| [ngrok](https://ngrok.com/) | ngrok secure introspectable tunnels to localhost webhook development tool and debugging tool. |
| [macdown](http://macdown.uranusjr.com/) | The open source Markdown editor for OS X. |
| [obs](https://obsproject.com/) | Free, open source software for live streaming and recording |
| [paw](https://luckymarmot.com/paw) | The ultimate HTTP client for Mac |
| [qlcolorcode](https://code.google.com/p/qlcolorcode/) | A Quick Look plugin for source code with syntax highlighting |
| [qlmarkdown](https://github.com/toland/qlmarkdown) | QuickLook generator for Markdown files. |
| [qlstephen](http://whomwah.github.io/qlstephen/) | A QuickLook plugin that lets you view plain text files without a file extension |
| [recordit](http://recordit.co/) | Record screencasts fast & free! with GIF Support! |
| [robomongo](http://robomongo.org/) | Shell-centric cross-platform MongoDB management tool |
| [sketch](http://bohemiancoding.com/sketch/) | Sketch gives you the power, flexibility and speed you always wanted in a lightweight and easy-to-use package. |
| [sketch-toolbox](http://sketchtoolbox.com/) | A super simple plugin manager for Sketch |
| [skype](http://sketchtoolbox.com/) | 用Skype 免費與親朋好友保持聯繫。立即下載Skype，用電腦及行動裝置聊天及撥號。 |
| [slack](https://slack.com/) | A messaging app for teams. |
| [sourcetree](http://www.sourcetreeapp.com/) | A free Git & Mercurial client for Windows or Mac. |
| [spectacle](https://www.spectacleapp.com/) | Spectacle allows you to organize your windows without using a mouse. |
| [spotify](https://www.spotify.com/) | SSpotify 是一種數碼音樂服務，讓你能收聽過百萬首歌曲。 |
| [steam](http://store.steampowered.com/) | Digital game store for Windows, Mac and Linux platforms with forums, update client and store code redemtion. |
| [sublime-text3](http://www.sublimetext.com/3) | Sublime Text is a sophisticated text editor for code, markup and prose. |
| [tiled](http://www.mapeditor.org/) | Your free, easy to use and flexible tile map editor. |
| [telegram](https://telegram.org/) | a new era of messaging |
| [unity](http://unity3d.com/) | Unity is the ultimate game development platform. |
| [utorrent](http://www.utorrent.com/) | uTorrent is the #1 BitTorrent download client on desktops worldwide. |
| [virtualbox](https://www.virtualbox.org/) | VirtualBox is a powerful x86 and AMD64/Intel64 virtualization product for enterprise as well as home use |
| [visual-studio-code](https://code.visualstudio.com/) | Build and debug modern web and cloud applications. |
| [vlc](http://www.videolan.org/vlc/) | VLC 是一個自由和開源的跨平台多媒體播放器和框架，可以播放大多數多媒體檔案，以及 DVD、音樂CD、VCD 和各種串流協定。 |
| [webkit-nightly](https://webkit.org/) | Open Source Web Browser Engine |
| [webstorm](https://www.jetbrains.com/webstorm/) | The smartest JavaScript IDE |

剩下無法透過 Homebrew 安裝，或是需要透過 App Store 購買的應用程式，只能手動一個一個安裝回來了...

以下是目前我安裝的應用程式：

### App Store

| name | 說明 |
| --- | --- |
| [Affinity Photo](https://affinity.serif.com/en-us/photo/) | Professional photo editing software for Mac |
| [Dash](https://kapeli.com/dash) | Dash gives your Mac instant offline access to 150+ API documentation sets |
| [GIFMaker](https://itunes.apple.com/us/app/gifmaker-easily-create-gif/id1015930892) | easily create a GIF from a video or images |
| [LINE](http://line.me/) | LINE 是一款全新型態的通訊應用程式，讓您隨時隨地享受免費傳訊、免費通話等溝通樂趣！ |
| [Gestimer](http://maddin.io/gestimer/) | For those little reminders during the day |
| [Todoist](https://todoist.com/) | To-do list and task manager. Free, easy, online and mobile |

### OS X defaults setting

執行 `$ ./osx/set-defaults.sh` 之後，程式會將 Mac OS X 的一些系統設置改變，可以根據個人需求修改這個檔案，或是參考 [Mathias’s dotfiles](https://github.com/mathiasbynens/dotfiles/blob/master/.osx) 整理好的配置。

以下是目前設定的配置：

| setting |
| ------ |
| 關閉電池進入深入睡眠模式 |
| 關閉電源進入深入睡眠模式 |
| 加快視窗 resize 的速度(Cocoa applications) |
| 預設展開儲存視窗 |
| 關閉“你確定要開啟這個應用程式?”詢問視窗 |
| 關閉 Time Machine |
| 加速進入睡眠模式 |
| 開啟觸控板輕觸點擊功能 |
| 開啟觸控板/滑鼠右鍵選單功能 |
| 開啟觸控板三指拖曳功能 |
| 開啟觸控板四指向下滑出現 app expose 功能 |
| 加快觸控板/滑鼠的速度 |
| 開啟全部視窗組件支援鍵盤控制 |
| 關閉鍵盤按住的輸入限制 |
| 加快鍵盤輸入 |
| 移除視窗截圖的影子 |
| 預設 Finder 起始位置為下載資料夾 |
| 顯示副檔名 |
| 顯示 Finder 狀態列 |
| 顯示 Finder 路徑列 |
| 允許框選 Finde Quick Look 的文字 |
| Finder 標題列顯示完整路徑 |
| 預設搜尋列的結果為當前目錄下 |
| 關閉改變副檔名的警告提示 |
| 開啟資料夾的 spring loading 功能 |
| 開啟 Dock 的 spring loading 功能 |
| 移除 spring loading 的延遲 |
| 避免在 network volumes 底下建立 .DS_Store 檔案 |
| 使用 column view 作為 Finder 預設顯示選項 |
| 關閉清空垃圾桶的警告提示 |
| 使用黑色的選單列和 Dock |
| 使用縮放的效果作為視窗放大縮小效果 |
| 應用程式縮小至自己的圖示 |
| 顯示 Dock 應用程式開啟中的小亮燈提示 |
| 關閉 Dock 開啟應用程式的彈跳動畫 |
| 加快 Mission Control 的動畫速度 |
| 關閉 Mission Control 的應用程式群組化顯示 |
| 關閉 Dashboard |
| 將 Dashboard 從多重桌面之中移除 |
| 自動隱藏 Dock |
| 移除隱藏 Dock 的延遲 |
| 移除 Dock 的顯示/隱藏動畫 |
| 將隱藏的應用程式 Dock 圖示半透明顯示 |

以上，若修改過 `homebrew/install.sh` 或 `osx/set-defaults.sh` 之後，直接執行指令:

```bash
$ dot
```

就會再次更新 packages 還有 defaults setting。

## Mackup

當初始環境都安裝好之後，剩下的就是恢復備份。除了 `.zsrc`、`.vimrc` 這類 dotfile 比較適合放在版本控制之外，其他像是 Sublime 的 plugin、iTerm2 的 setting、Oh My Zsh 的 plugin、等等很多還有一般應用程式的配置檔需要備份，甚至是 SSH 的 key，這些我認為都不適合丟進 dotfiles 放上 GitHub。所以這裡介紹 [Mackup](https://github.com/lra/mackup) 這個簡單的工具作為解決方案，使用方式很簡單，`brew install mackup` 安裝完之後只要執行：

```bash
$ mackup backup
```

就可以將檔案備份到 Dropbox 或 Google Drive。當需要恢復的時候則是執行:

```bash
$ mackup restore
```

就會將雲端硬碟上的備份以 `ln` 連結的方式在新電腦上同步。

配置方式也很容易，建立一份 `~/.mackup.cfg`，或是直接使用 `.dofiles/mackup/mackup.cfg.symlink` 來修改:

```bash
[storage]
engine = dropbox # 同步的雲端硬碟，有 dropbox 與 google_drive 可以選擇
directory = Mackup # 同步的資料夾，這裡會將所有備份同步至 ~/Dropbox/Mackup 底下

# 指定要同步的應用程式
[applications_to_sync]
iterm2
oh-my-zsh
sublime-text-3
ssh

[applications_to_ignore]
# 指定不想同步的應用程式
```

以下是目前我備份的應用程式：

| app |
| --- |
| aws |
| flux |
| iterm2 |
| moom |
| oh-my-zsh |
| sourcetree |
| sublime-text-3 |
| ssh |

更多詳細的配置與支援的軟體請參閱 [mackup 的文件](https://github.com/lra/mackup/tree/master/doc)。

## Reference

- [Hacker's Guide to Setting up Your Mac](http://lapwinglabs.com/blog/hacker-guide-to-setting-up-your-mac)
- [First steps with Mac OS X as a Developer](http://carlosbecker.com/posts/first-steps-with-mac-os-x-as-a-developer/)
- [Mac 开发配置手册](https://www.gitbook.com/book/aaaaaashu/mac-dev-setup/details)
- [OS X Yosemite Security and Privacy Guide](https://github.com/drduh/OS-X-Yosemite-Security-and-Privacy-Guide)
- [强迫症的 Mac 设置指南](https://github.com/macdao/ocds-guide-to-setting-up-mac)
- [awesome-osx-command-line](https://github.com/herrbischoff/awesome-osx-command-line)

## Thanks

I forked [Zach Holman](http://github.com/holman)'s excellent [dotfiles](http://github.com/holman/dotfiles).
