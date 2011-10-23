# Sublime Text 2 Configuration (en)

This repository contains my Sublime Text 2 configurations.

## Plugins

Here are the plugins im using:

* Django for SublimeText 2 (https://github.com/squ1b3r/Djaneiro)
* Sniptastic (https://github.com/bobthecow/sublime-sniptastic)
* Soda Theme (https://github.com/buymeasoda/soda-theme)
* SublimeCodeIntel (https://github.com/Kronuz/SublimeCodeIntel)
* SublimeLinter (https://github.com/Kronuz/SublimeLinter)
* Github GISTs (https://github.com/bgreenlee/sublime-github)
* BracketHighlighter (https://github.com/facelessuser/BracketHighlighter)
* GitHub for SublimeText 2 (https://github.com/kemayo/sublime-text-2-git)
* ZenCoding (https://bitbucket.org/sublimator/sublime-2-zencoding)

You can install the above plugins you can use PackageControl default repository
channel, for the ones bellow:

* Jinja2 (https://github.com/mitsuhiko/jinja2-tmbundle)
* GoSublime (https://github.com/DisposaBoy/GoSublime)

You need to use (for now) my repository channel file:

```
https://raw.github.com/douglas/package_control_channel/master/repositories.json
```

## How to use it

* In fact, you just have to look at the files and adapt your own files to
  my configs =)

## System configurations

* Note that i do not have a "Base File.sublime-settings" in the repository,
  instead, i have config files for each architecture - so you just need to
  do a symbolic link of the platform file to the "Base File.sublime-settings"
  file:

```bash
$ ln -s "Base File (<plataform>).sublime-settings" "Base File.sublime-settings"
```

## SublimeCodeIntel configuration (autocomplete and go to definition)

* To use SublimeCodeIntel, install it using @wbond Package Control and do
  the following:

```bash
$ mkdir ~/.codeintel
$ touch ~/.codeintel/config
```

* Edit the file ``~/.codeintel/config`` e put something like this:

```json
{
    "Python": {
        "python": '/your/python/interpreter/directory/bin/python',
        "pythonExtraPaths": ['/the/root/of/your/project/directory/',
                             '/another/root/of/your/project/directory/',
        ]
    },
}
```

In the ``python``, you need to define the path to the interpreter that you want
to use (virtualenv interpreter works too), in ``pythonExtraPaths`` you may want
to put the path of your projects (to use autocomplete and go_to_definition)

# Configurações do Sublime Text 2 (pt-br)

Esse repositório contém as minhas configurações do Sublime Text 2.

## Plugins

Esses são os plugins que estou usando:

* Django for SublimeText 2 (https://github.com/squ1b3r/Djaneiro)
* Sniptastic (https://github.com/bobthecow/sublime-sniptastic)
* Soda Theme (https://github.com/buymeasoda/soda-theme)
* SublimeCodeIntel (https://github.com/Kronuz/SublimeCodeIntel)
* SublimeLinter (https://github.com/Kronuz/SublimeLinter)
* Github GISTs (https://github.com/bgreenlee/sublime-github)
* BracketHighlighter (https://github.com/facelessuser/BracketHighlighter)
* GitHub for SublimeText 2 (https://github.com/kemayo/sublime-text-2-git)
* ZenCoding (https://bitbucket.org/sublimator/sublime-2-zencoding)

Você pode instalar os plugins acima utilizando o canal de repositórios padrão
do PackageControl. Para os plugins abaixo:

* Jinja2 (https://github.com/mitsuhiko/jinja2-tmbundle)
* GoSublime (https://github.com/DisposaBoy/GoSublime)

Você precisa utilizar (por agora) o meu canal de repositórios:

```
https://raw.github.com/douglas/package_control_channel/master/repositories.json
```

## Como utilizar

* Você precisa apenar olhar os arquivos de configuração e adaptá-los para as
  suas necessidades =)

## Configurações do sistema

* Observe que não tenho um arquivo "Base File.sublime-settings" nesse
  repositório, ao invés disso, eu tenho arquivos de configuração para cada
  arquitetura - você só precisa criar um link simbólico do arquivo da sua
  plataforma para: "Base File.sublime-settings":

```bash
$ ln -s "Base File (<plataform>).sublime-settings" "Base File.sublime-settings"
```

## Configurações do SublimeCodeIntel (autocomplete e go to definition)

* Para utilizar SublimeCodeIntel, instale-o utilizando Package Control do
  @wbond e faça o seguinte:

```bash
$ mkdir ~/.codeintel
$ touch ~/.codeintel/config
```

* Altere o arquivo ``~/.codeintel/config`` e coloque algo como:

```json
{
    "Python": {
        "python": '/seu/diretorio/do/interpretador/python/bin/python',
        "pythonExtraPaths": ['/a/raiz/do/seu/diretorio/de/projeto/',
                             '/outra/raiz/do/seu/diretorio/de/projeto/',
        ]
    },
}
```

Para a chave ``python``, defina o caminho para o interpretador que você deseja
utilizar (pode ser virtualenv), em ``pythonExtraPaths`` você pode colocar
o caminho do seu projeto (para utilizar autocomplete e go_to_definition)














