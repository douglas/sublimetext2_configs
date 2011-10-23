# Sublime Text 2 Configuration (en)

TODO: Translate the portuguese contents below, sorry.


# Configuração do Sublime Text 2 (pt_br)

Esse projeto armazena as minhas configurações e os plugins que eu uso no
Sublime Text 2.

## Plugins

* Django for SublimeText 2 (https://github.com/squ1b3r/Djaneiro)
* Sniptastic (https://github.com/bobthecow/sublime-sniptastic)
* Soda Theme (https://github.com/buymeasoda/soda-theme)
* SublimeCodeIntel (https://github.com/Kronuz/SublimeCodeIntel)
* SublimeLinter (https://github.com/Kronuz/SublimeLinter)
* SublimeGitHub (https://github.com/bgreenlee/sublime-github)
* GoSublime (https://github.com/DisposaBoy/GoSublime)
* BracketHighlighter (https://github.com/facelessuser/BracketHighlighter)
* GitHub for SublimeText 2 (https://github.com/kemayo/sublime-text-2-git)
* Jinja2 (https://github.com/mitsuhiko/jinja2-tmbundle)
* ZenCoding (https://bitbucket.org/sublimator/sublime-2-zencoding)
...

## Instalação

* Faça uma backup da pasta ``User`` e apague-a (iremos clonar as minhas configs)

* Faça o clone desse projeto dentro da pasta ``Packages`` definindo o nome da
pasta como ``User``:

```bash
$ git clone https://douglas@github.com/douglas/sublimetext2_configs.git User
```

## Setup automático

O @santagada fez um shellscript para facilitar a instalação, prefira executá-lo
ser for a primeira vez que você usa essas configurações

```bash
$ sh setup.sh
```

Isso deve bastar =)

## Setup manual

* Entre na pasta ``User`` e depois faça o download dos submódulos:

```bash
$ cd User
$ git submodule init
$ git submodule update
```

* Fazer os links simbolicos para os submódulos que estão em User dentro da
pasta Packages (coloquei dessa forma para facilitar o versionamento)

### osx

```bash
$ cd ~/Library/Application Support/Sublime Text 2/Packages
```
### gnu/linux

```bash
$ cd ~/.config/sublime-text-2/Packages
```

### Criação dos links

```bash
$ ln -s User/BracketHighlighter .
$ ln -s User/Sniptastic .
$ ln -s User/SublimeLinter .
$ ln -s User/SublimeCodeIntel .
$ ln -s User/Djaneiro .
$ ln -s "User/Theme - Soda" .
$ ln -s User/jinja2-tmbundle Jinja2
$ ln -s User/sublime-github .
$ ln -s User/sublime-text-2-git Git
```

### ZenCoding

O ZenCoding está hospedado em um repositório Mercurial, portanto para
atualizá-lo basta executar o seguinte comando:

$ cd ZenCoding
$ hg pull -u

## Atualização dos submódulos

Para atualizar todos os submódulos de uma só vez, execute o seguinte comando:

```bash
$ git submodule foreach git pull origin master
```

## Configurações do sistema

* Crie um link simbólico para que as configuracoes gerais sejam vistas. Faça de
acordo com sua plataforma (OSX ou Linux):

```bash
$ ln -s "Base File (<plataforma>).sublime-settings" "Base File.sublime-settings"
```

## Configuração do SublimeCodeIntel (autocomplete e go to definition)

* Para utilizar o SublimeCodeIntel, execute os seguintes comandos:

```bash
$ mkdir ~/.codeintel
$ touch ~/.codeintel/config
```

* Edite o arquivo ``~/.codeintel/config`` e coloque algo assim:

```json
{
    "Python": {
        "python": '/Users/douglas/work/ambientes/django/bin/python',
        "pythonExtraPaths": ['/Users/douglas/work/ambientes/django/lib/python2.7/site-packages',
                             '/usr/local/Cellar/python/2.7.2/lib/python2.7/site-packages',
                             '/Users/douglas/work/sid/devel',
                             '/Users/douglas/work/sid/devel/apps_logicas',
                             '/Users/douglas/work/sid/devel/contrib',
                             '/Users/douglas/work/sid/devel/sid',
                             '/Users/douglas/work/sid/devel/sid/apps'
        ]
    },

}
```

Em ``python``, você precisa definir o caminho do interpretador que você irá usar,
em ``pythonExtraPaths`` os caminhos onde teus módulos e sistemas estão
instalados (para usar o autocomplete e go_to_definition)
