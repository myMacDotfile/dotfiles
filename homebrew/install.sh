# !/bin/sh
#
# Homebrew
#
# This installs some of the common dependencies needed (or at least desired)
# using Homebrew.

# Binaries
binaries=(
  git-flow
  grc
  httpie
  hub
  legit
  mackup
  mongodb
  nvm
  opencc
  ssh-copy-id
  trash
  tree
  youtube-dl
)

# Apps
apps=(
  alfred
  atom
  dockertoolbox
  dropbox
  firefox
  flux
  github-desktop
  google-chrome
  heroku-toolbelt
  istat-menus
  iterm2
  keka
  neteasemusic
  macdown
  obs
  qlcolorcode
  qlmarkdown
  qlstephen
  qq
  recordit
  robomongo
  sketch
  slack
  sourcetree
  steam
  sublime-text3
  todoist
  unity
  virtualbox
  vlc
)

# Fonts
fonts=(
  font-noto-sans-japanese
  font-noto-sans-korean
  font-noto-sans-s-chinese
  font-noto-sans-t-chinese
  font-roboto
  font-source-code-pro
)

echo "Update Homebrew..."
# Update homebrew recipes
brew update

# Install GNU core utilities (those that come with OS X are outdated)
brew install coreutils
# Install GNU `find`, `locate`, `updatedb`, and `xargs`, g-prefixed
brew install findutils
# Install Bash 4
brew install bash
# Install Homebrew Cask
brew tap caskroom/fonts
brew tap caskroom/versions
brew install caskroom/cask/brew-cask
brew upgrade brew-cask

echo "Do you want to install or update Homebrew binaries?"
select yn in "Yes" "No"; do
  case $yn in
    Yes )
      echo "Installing binaries...";
      brew install ${binaries[@]};
      break;;
    No ) break;;
  esac
done

echo "Do you want to install fonts by Homebrew Cask?"
select yn in "Yes" "No"; do
  case $yn in
    Yes )
      echo "Installing fonts...";
      brew cask install ${fonts[@]};
      break;;
    No ) break;;
  esac
done

echo "Do you want to install or update applications by Homebrew Cask?"
select yn in "Yes" "No"; do
  case $yn in
    Yes )
      # Install apps to /Applications
      # Default is: /Users/$user/Applications
      echo "Installing apps..."
      sudo brew cask install --appdir="/Applications" ${apps[@]}
      break;;
    No ) break;;
  esac
done

# clean things up
brew cleanup
brew cask cleanup

exit 0
