<#
.SYNOPSIS
  Installa il plugin camunda-mcp nel Camunda Desktop Modeler (Windows).

.DESCRIPTION
  Scarica il pacchetto pronto dalla pagina Releases di JesseLeresche/Camunda-mcp,
  lo estrae e lo copia in  %APPDATA%\camunda-modeler\resources\plugins\camunda-mcp
  Il pacchetto v2 non contiene moduli nativi: nessuna build, nessun Node richiesto.

.PARAMETER Version
  Tag della release da installare. Default: v2.0.0

.PARAMETER Latest
  Interroga GitHub e installa l'ultima release disponibile (ignora -Version).

.PARAMETER ModelerData
  Cartella dati del Modeler. Default: $env:APPDATA\camunda-modeler

.PARAMETER Force
  Sovrascrive un'installazione esistente senza chiedere conferma.

.EXAMPLE
  .\install-camunda-mcp.ps1
.EXAMPLE
  .\install-camunda-mcp.ps1 -Latest -Force
#>
[CmdletBinding()]
param(
  [string]$Version = "v2.0.0",
  [switch]$Latest,
  [string]$ModelerData = (Join-Path $env:APPDATA "camunda-modeler"),
  [switch]$Force
)

$ErrorActionPreference = "Stop"
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}
$repo = "JesseLeresche/Camunda-mcp"

Write-Host "Plugin camunda-mcp -> Camunda Desktop Modeler" -ForegroundColor Cyan

if (-not (Test-Path $ModelerData)) {
  Write-Warning "Cartella dati del Modeler non trovata: $ModelerData"
  Write-Warning "Avvia una volta il Camunda Modeler, oppure passa -ModelerData <percorso>."
  exit 1
}

if ($Latest) {
  Write-Host "Cerco l'ultima release..."
  $rel = Invoke-RestMethod "https://api.github.com/repos/$repo/releases/latest" -Headers @{ "User-Agent" = "install-camunda-mcp" }
  $Version = $rel.tag_name
}
$zipName = "camunda-mcp-$Version.zip"
$url = "https://github.com/$repo/releases/download/$Version/$zipName"
Write-Host "Release:  $Version"
Write-Host "Sorgente: $url"

$work = Join-Path ([IO.Path]::GetTempPath()) ("camunda-mcp-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $work | Out-Null
$zip = Join-Path $work $zipName
try {
  Write-Host "Scarico..."
  Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  Write-Host "Estraggo..."
  Expand-Archive -Path $zip -DestinationPath $work -Force

  $src = Join-Path $work "camunda-mcp"
  if (-not (Test-Path (Join-Path $src "index.js"))) {
    throw "Struttura dell'archivio inaspettata: manca camunda-mcp\index.js"
  }

  $pluginsDir = Join-Path $ModelerData "resources\plugins"
  $dest = Join-Path $pluginsDir "camunda-mcp"
  New-Item -ItemType Directory -Path $pluginsDir -Force | Out-Null

  if (Test-Path $dest) {
    if (-not $Force) {
      $ans = Read-Host "Esiste gia' $dest - sovrascrivo? [s/N]"
      if ($ans -notmatch '^[sSyY]') { Write-Host "Annullato."; exit 0 }
    }
    Remove-Item -Recurse -Force $dest
  }

  Write-Host "Copio in $dest ..."
  Copy-Item -Recurse -Force $src $dest

  $ver = (Get-Content (Join-Path $dest "package.json") -Raw | ConvertFrom-Json).version
  Write-Host ""
  Write-Host "Installato: camunda-modeler-mcp-plugin $ver" -ForegroundColor Green
  Write-Host ""
  Write-Host "Prossimi passi:"
  Write-Host "  1. Riavvia il Camunda Desktop Modeler."
  Write-Host "  2. Menu Plugins -> deve comparire 'MCP Server: Running (port 3100)'."
  Write-Host "  3. Nel progetto, in .mcp.json:"
  Write-Host '       { "mcpServers": { "camunda-modeler": { "type": "http", "url": "http://localhost:3100/mcp" } } }'
  Write-Host "  4. Per il deploy su Camunda 8: imposta ZEEBE_ADDRESS=localhost:26500 prima di avviare il Modeler."
}
finally {
  Remove-Item -Recurse -Force $work -ErrorAction SilentlyContinue
}
