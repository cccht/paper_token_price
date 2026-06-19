param(
    [string]$OutputDir = $PSScriptRoot,
    [string]$BaseName = "information_interaction_visio"
)

$ErrorActionPreference = "Stop"
$PageW = 13.5; $PageH = 6.0
$Black  = "RGB(0,0,0)"; $DGray = "RGB(70,70,70)"; $LGray = "RGB(160,160,160)"
$White  = "RGB(255,255,255)";  $Bg    = "RGB(248,248,248)"

function Y([double]$y) { return $script:PageH - $y }

function Set-Cell($s,[string]$c,[string]$v) { try{$s.CellsU($c).FormulaU=$v}catch{} }

function Rect($x,$y,$w,$h,$fill,$line,$lw=1.2,$round=0.08,$dash=$false) {
    $s=$script:Page.DrawRectangle($x,(Y ($y+$h)),($x+$w),(Y $y))
    Set-Cell $s "FillForegnd" $fill; Set-Cell $s "FillPattern" "1"
    Set-Cell $s "LineColor" $line; Set-Cell $s "LineWeight" "$lw pt"
    Set-Cell $s "Rounding" "$round in"
    if($dash){Set-Cell $s "LinePattern" "2"}
    return $s
}

function Text($x,$y,$w,$h,$body,$size,$color,$bold=$false,$align=1) {
    $s=$script:Page.DrawRectangle($x,(Y ($y+$h)),($x+$w),(Y $y))
    Set-Cell $s "FillPattern" "0"; Set-Cell $s "LinePattern" "0"
    $s.Text=$body
    Set-Cell $s "Char.Font" "FONT(""Calibri"")"; Set-Cell $s "Char.Size" "$size pt"
    Set-Cell $s "Char.Color" $color; Set-Cell $s "Para.HorzAlign" "$align"; Set-Cell $s "VerticalAlign" "1"
    Set-Cell $s "LeftMargin" "0.06 in"; Set-Cell $s "RightMargin" "0.06 in"
    if($bold){Set-Cell $s "Char.Style" "1"}else{Set-Cell $s "Char.Style" "0"}
    return $s
}

function Arrow($x1,$y1,$x2,$y2,$dash=$false,$lw=1.3) {
    $s=$script:Page.DrawLine($x1,(Y $y1),$x2,(Y $y2))
    Set-Cell $s "LineColor" $DGray; Set-Cell $s "LineWeight" "$lw pt"
    Set-Cell $s "EndArrow" "13"
    if($dash){Set-Cell $s "LinePattern" "2"}
    return $s
}

function Block($x,$y,$w,$h,$title,$sub,$dash=$false) {
    Rect $x $y $w $h $Bg $Black 1.2 0.08 $dash | Out-Null
    Text ($x+0.12) ($y+0.10) ($w-0.24) 0.28 $title 12 $Black $true 0 | Out-Null
    Text ($x+0.12) ($y+0.42) ($w-0.24) ($h-0.56) $sub 9.5 $DGray $false 0 | Out-Null
}

function Label($x,$y,$txt,$size,$bold) {
    Text $x $y 4.0 0.28 $txt $size $DGray $bold 0
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$vsdx=Join-Path $OutputDir "$BaseName.vsdx"
$pdf=Join-Path $OutputDir "$BaseName.pdf"

$visio=New-Object -ComObject Visio.Application; $visio.Visible=$false; $visio.AlertResponse=7
$doc=$visio.Documents.Add("")
$script:Page=$visio.ActivePage
$script:Page.PageSheet.CellsU("PageWidth").ResultIU=$PageW
$script:Page.PageSheet.CellsU("PageHeight").ResultIU=$PageH
$script:Page.Name="Information Interaction"

# ── Section labels ────────────────────────────
Label 0.50 0.08 "Exogenous Input"         10 $true
Label 4.80 0.08 "Upper Layer (Platform)"   10 $true
Label 9.00 0.08 "Middle Layer (Brokers)"    10 $true
Label 9.00 2.80 "Lower Layer (Users)"       10 $true
Label 4.80 2.80 "QoS & Diagnostics"         10 $true

# ── Separator lines ──────────────────────────
Rect 0.35 0.42 13.0 0.01 $White $LGray 0.5 0 | Out-Null
Rect 0.35 3.15 13.0 0.01 $White $LGray 0.5 0 | Out-Null

# ── Row 1 ────────────────────────────────────
Block 0.40  0.65 3.60 1.60 "Exogenous API Supply"            "Token capacity, API cost, reliability inputs"                                            $true
Block 4.60  0.65 3.60 1.60 "Stage 1: Platform"               "Wholesale price w_t; anticipates responses"                                             $false
Block 8.80  0.65 4.30 1.60 "Stage 2: API Brokers"            "Retail price p_jt; allocate capacity g_jt"                                             $false

# ── Row 2 ────────────────────────────────────
Block 1.20  3.50 4.20 1.80 "Objective Diagnostics"           "Platform / broker / system payoff; user inclusive value as diagnostic"                 $true
Block 5.80  3.50 4.20 1.80 "QoS Monitor"                     "u_jt, q_jt; served demand D_jt * q_jt"                                                 $false
Block 10.40 3.50 2.70 1.80 "Stage 3: Users"                  "Broker x period choice; cross-period migration"                                        $false

# ── Arrows ────────────────────────────────────
Arrow 4.00  1.45  4.60 1.45   # supply→platform
Arrow 8.20  1.45  8.80 1.45   # platform→broker
Arrow 11.75 2.25 11.75 3.50   # broker→user
Arrow 11.75 5.30 10.00 5.30   # user→monitor
Arrow 5.80  5.30  5.40 5.30   # monitor→revenue
Arrow 3.30  3.50  6.50 2.25  $true  # feedback (dashed)
Text  4.10 2.50 3.0 0.28 "Feedback loop" 9 $DGray $true 1

$doc.SaveAs($vsdx)
$doc.ExportAsFixedFormat(1,$pdf,1,0)
$doc.Close(); $visio.Quit()
Write-Output "Generated: $vsdx`n$pdf"
