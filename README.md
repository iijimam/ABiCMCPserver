# ABiC-MCPServer

[*InterSystems Demo Games*](https://community.intersystems.com/node/584222)

東京 SE チーム提出のサンプルコードです。

このリポジトリには、MCP サーバ用コードのみが含まれています。

呼び出し先となる REST API のコード一式は [https://github.com/Intersystems-jp/demogames-tokyo](https://github.com/Intersystems-jp/demogames-tokyo) にあります。

---
~English~
This is sample code submitted by the Tokyo SE team.

This repository contains only code for the MCP server.

The complete set of code for the REST API to be called is available at [https://github.com/Intersystems-jp/demogames-tokyo](https://github.com/Intersystems-jp/demogames-tokyo).

## Components

MCP サーバ名：ABiCMCPServer で作成しています。

MCP サーバに含まれるツールは以下の通りです。

---
~Enblish~

MCP server name is **ABiCMCPServer**.

The tools included in the MCP server are as follows.

### Tools

この MCP サーバに含まれるツールは以下の通りです。

~English~

The following tools are included in this MCP server.

- dashboard

  自然言語で分析内容を指示すると、内容に沿ったピボットを表示するダッシュボードが作成されます。
  
  前提：接続先の IRIS BI に事前定義された分析モデル（キューブ）に対してのみ実行できます。

  **Claude desktop のチャット**に、自然言語で分析内容を送付すると実行できます。

  ~English~

  When you specify the analysis content in natural language, a dashboard displaying pivots based on that content will be created.
  
  Prerequisite: This can only be executed for predefined analysis models (cubes) in the connected IRIS BI.

  You can execute this by sending the analysis content in natural language to the **Claude desktop chat**.

  - Ex1：2024年4月の障害レベル別、継続度別、インシデントレポート件数を教えて
  
    Tell me the number of incident reports by fault level, continuity and number of incident reports in April in 2024.


  - Ex2：2024年4月の従業員の役割別、夜勤、日勤数を教えて
  
    Tell me the number of employees, by role, working nights and days in April in 2024.


## Quickstart

### Install

#### Claude Desktop configulation

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

**※ディレクトリには、リポジトリ clone 後のディレクトリのフルパスを指定してください。**

~English~

**Please specify the full path of the directory after cloning the repository in the directory.**

```
"mcpServers": {
  "ABiCMCPServer": {
    "command": "uv",
    "args": [
      "--directory",
      "C:\\WorkSpace\\MCPTest\\ABiCMCPserver",
      "run",
      "ABiCMCPServer"
    ]
  }
}
```
