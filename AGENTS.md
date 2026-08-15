# Contexto do usuário

- O usuário é **Oficial da Polícia Militar do Estado de São Paulo (PMESP)** no posto de **Capitão PM**.
- Sempre que uma resposta puder ser direcionada por posto/graduação, priorize as regras aplicáveis a **Capitão PM**.

## Regulamento de uniformes (R-5-PM)

O principal manual de referência do projeto é o **R-5-PM, 6ª Ed. v.2** (Regulamento de Uniformes da PMESP).

**Onde ele está:** no Google Drive, não neste repositório.

```
G:\Meu Drive\10_JOSEMAR\02_TRABALHO\P1\Manuais\R-5-PM 6ª Ed. v.2_RU_Port 2 e 4 de 26_bvp.pdf
G:\Meu Drive\10_JOSEMAR\02_TRABALHO\P4\R-5-PM 6ª Ed. v.2_RU_Port 2 e 4 de 26_bvp.pdf
```

As duas cópias têm o mesmo conteúdo (texto idêntico, 420 páginas). O md5 difere só
por recompressão do PDF.

Também existe uma cópia local em `Manuais/`, que o `.gitignore` mantém fora do
git. Se a pasta não existir na máquina em que você está, use o caminho do Drive
acima.

**Por que fora do repositório:** este repositório é **público** (exigência do
GitHub Pages gratuito, que publica o painel). O R-5-PM tem 37 MB e é documento
de circulação interna da corporação, então não deve ser redistribuído em página
pública nem inflar o repositório de forma permanente, já que o git guarda para
sempre o que entra. Decisão tomada em 06/08/2026.

**Ao consultar o R-5-PM, foque em:**

- **Uniformes** (padrões, composições e ocasiões de uso);
- **Insígnias** de Capitão PM;
- **Distintivos** de Capitão PM;
- Regras específicas para **oficiais** quando houver diferença em relação às praças.

Responda com base no texto do regulamento. Cite o artigo/item ou seção quando
possível. Se a informação não estiver clara no texto, indique a incerteza antes
de responder.

**Ler o desenho, não só o texto (aprendido em 15/08/2026).** As figuras do R-5-PM
fazem parte da norma e trazem itens que o texto do artigo não enumera. Exemplo real:
o Art. 93, § 3º lista os ornamentos obrigatórios do paletó e não cita as mangas, mas
o desenho do § 1º mostra a Bandeira de São Paulo na manga direita e a Logomarca da
PMESP na esquerda. Quem lê só o texto extraído erra. Antes de afirmar que uma peça
"não leva" algum distintivo, renderize a página e olhe:

```
pdftotext -layout -enc UTF-8 "<pdf>" saida.txt      # achar o artigo
pdftoppm -f <pag> -l <pag> -r 200 -png "<pdf>" img  # olhar a figura
```

A numeração impressa do RU fica cerca de 3 páginas atrás da numeração do PDF.

**Uso mais frequente hoje:** conferir os itens de uniforme das abas
[Compras](COMPRAS.md) e [Mala](MALA.md), que listam as peças a levar para o CAO
(a conferência de armário foi concluída em 06/08/2026). As referências
de artigo já registradas em [ROTINA.md](ROTINA.md) (P-1 no Art. 45, B-1 no
Art. 23, jaqueta de passeio no Art. 127, camiseta de serviço no Art. 74) vieram
desse regulamento e podem ser conferidas nele.
