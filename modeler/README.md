# Installazione del plugin camunda-mcp nel Modeler

Il **Camunda Desktop Modeler** è installato sul PC (non in Docker). Il plugin
`camunda-mcp` gli aggiunge un server MCP HTTP su `localhost:3100` con cui un
assistente (Claude) crea e modifica i diagrammi BPMN dai prompt.

Fonte: <https://github.com/JesseLeresche/Camunda-mcp> (licenza MIT). Il pacchetto
pronto `v2.0.0` contiene solo JavaScript: nessuna build, nessun Node richiesto.

## Windows (PowerShell)

Il Modeler gira su Windows: usare lo script PowerShell.

```powershell
# dalla cartella modeler\ del progetto
powershell -ExecutionPolicy Bypass -File .\install-camunda-mcp.ps1
```

Opzioni: `-Latest` (ultima release), `-Version v2.0.0`, `-Force` (sovrascrivi),
`-ModelerData <percorso>` (default `%APPDATA%\camunda-modeler`).

## WSL / Linux (bash)

Rileva `%APPDATA%` di Windows tramite `cmd.exe` e copia il plugin lì.

```bash
./install-camunda-mcp.sh              # release pinnata v2.0.0
./install-camunda-mcp.sh --latest     # ultima release
./install-camunda-mcp.sh --from-source  # git clone + npm run build (Node >=20 + git)
MODELER_DATA="$HOME/.config/camunda-modeler" ./install-camunda-mcp.sh   # Modeler nativo Linux
```

## Cosa fa lo script

1. Individua la cartella dati del Modeler (`%APPDATA%\camunda-modeler`).
2. Scarica ed estrae `camunda-mcp-<versione>.zip`.
3. Copia la cartella `camunda-mcp/` in `…\resources\plugins\camunda-mcp`
   (sostituendo un'installazione precedente, con conferma se non si passa `--force`).

## Dopo l'installazione

1. Riavviare il Camunda Desktop Modeler.
2. Menu **Plugins** → deve comparire «MCP Server: Running (port 3100)».
3. Collegare il client, in `.mcp.json` del progetto:

   ```json
   { "mcpServers": { "camunda-modeler": { "type": "http", "url": "http://localhost:3100/mcp" } } }
   ```

4. Per distribuire su Camunda 8 (cartella `../camunda/`): impostare
   `ZEEBE_ADDRESS=localhost:26500` prima di avviare il Modeler.

Il flusso completo è descritto in `../site/lab-camunda-mcp.html`.

## Disinstallazione

Eliminare la cartella `…\camunda-modeler\resources\plugins\camunda-mcp` e riavviare
il Modeler.
