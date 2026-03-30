# JMComic-Crawler-Python-Lite

主使用核心:
```
pip install git+https://github.com/zakozakozakozakozako/JMComic-Crawler-Python-Lite
```
注:请先检查下方依赖是否正常安装

# Termux 运行说明

这个仓库的默认请求实现已经改成 `requests`，因此在 Termux 上不再强依赖 `curl_cffi`。

## 安装

```sh
pkg update && pkg upgrade
pkg install python git clang
python -m pip install -U pip setuptools wheel
```

如果你要安装图片处理和加密相关依赖，再补上常见的系统库：

```sh
pkg install libjpeg-turbo zlib freetype libwebp libpng libyaml openssl pkg-config
```

然后在项目根目录执行：

```sh
python -m pip install -e .
```

如果出现兼容异常你可能需要:
```
pkg reinstall libexpat
pkg reinstall python
pkg reinstall python-pip
```

或者只装运行依赖：

```sh
python -m pip install commonX requests PyYAML Pillow pycryptodome
```

## 运行

```sh
jmcomic 123456
```

查看详情：

```sh
jmv 123456
```

## 说明

- `commonX` 是纯 Python 包，适合 Termux。
- `curl-cffi` 更适合桌面平台；在 Termux 里更稳的做法是改用 `requests`。
- Termux 本身提供 Python，并且通过 `apt` 管理系统包、通过 `pip` 安装 Python 包。
