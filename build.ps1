Param(
    [parameter(mandatory=$true)][String]$adoc_file
)
$fmt_str="building... {0}";

Write-Output($fmt_str -f $adoc_file)
asciidoctor-pdf -r asciidoctor-pdf-linewrap-ja $adoc_file