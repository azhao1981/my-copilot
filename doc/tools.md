


## yek

## [lightpanda](https://github.com/lightpanda-io/browser)

无头浏览器，可以用来爬取网页

```bash
./lightpanda-x86_64-linux --dump https://lightpanda.io

lightpanda --dump https://lightpanda.io
```

Lightpanda 浏览器是一个开源的、为无头使用而设计的浏览器。它支持 JavaScript 执行、Web API（部分功能正在开发中）以及通过 CDP（Chrome DevTools Protocol）与 Playwright 和 Puppeteer 兼容。Lightpanda 的主要特点包括超低内存占用（比 Chrome 少 9 倍）和异常快的执行速度（比 Chrome 快 11 倍），同时具有瞬间启动能力。

要开始使用 Lightpanda，可以从每晚构建的版本中下载最新的二进制文件，支持 Linux x86_64 和 MacOS aarch64 平台。下载后，可以通过运行二进制文件来启动浏览器，如果提供了 URL，浏览器将获取该页面并退出；否则，它将启动一个 CDP 服务器。Lightpanda 提供了多个命令行选项，包括设置 CDP 服务器的主机和端口、设置超时时间以及在获取模式下将文档转储到标准输出。

Lightpanda 还支持通过 Puppeteer 脚本来控制浏览器。通过配置浏览器的 WebSocket 端点，用户可以连接到 Lightpanda 的 CDP 服务器并执行 Puppeteer 脚本。这种方式允许用户利用 Lightpanda 的高性能和低内存占用优势来进行网页自动化任务。

如果用户想要从源代码构建 Lightpanda，需要先安装 Zig 0.13.0，以及其他依赖项如 zig-js-runtime、Netsurf libs 和 Mimalloc。构建过程可以通过运行 make install 命令来完成，这将安装所有依赖项并构建 Lightpanda。用户也可以选择逐步构建依赖项，包括初始化和更新子模块、安装 Netsurf libs、Mimalloc 和 zig-js-runtime。

Lightpanda 提供了单元测试和 Web 平台测试（WPT）来确保其功能和兼容性。用户可以通过运行 make test 命令来执行单元测试，而 WPT 测试则需要额外的设置和配置。Lightpanda 的开发者还提供了一个用于执行 WPT 测试的专用仓库，用户可以通过 make install-submodule 命令来获取这些测试用例。

https://news.ycombinator.com/item?id=42817439

开发者应该优先考虑防止滥用工具，例如遵守 robot.txt 文件和限制请求频率
限制软件的功能会导致用户失去控制权，类似于数字版权管理（DRM）
开发者应该提供合理的默认设置和支持合乎道德的爬虫行为
限制软件的功能不会阻止恶意行为，只会给合法用户带来不便
添加 robot.txt 支持是双赢的解决方案，可以保护网站和用户的权益
开发者应该在默认设置中鼓励良好的行为，而不是强制限制用户的行为
