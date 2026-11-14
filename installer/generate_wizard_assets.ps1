Add-Type -AssemblyName System.Drawing
$ErrorActionPreference = 'Stop'
$dir = $PSScriptRoot
$white = [System.Drawing.Brushes]::White
$sf = [System.Drawing.StringFormat]::new()
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center

function Save-Bmp($bmp, $name) {
  $bmp.Save((Join-Path $dir $name), [System.Drawing.Imaging.ImageFormat]::Bmp)
}

# ============ WizardImage.bmp (164 x 314) ============
$w = 164; $h = 314
$bmp = [System.Drawing.Bitmap]::new($w, $h, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$p0 = [System.Drawing.Point]::new(0, 0)
$p1 = [System.Drawing.Point]::new($w, $h)
$c1 = [System.Drawing.Color]::FromArgb(37, 97, 199)
$c2 = [System.Drawing.Color]::FromArgb(15, 60, 140)
$lg = [System.Drawing.Drawing2D.LinearGradientBrush]::new($p0, $p1, $c1, $c2)
$rect = [System.Drawing.Rectangle]::new(0, 0, $w, $h)
$g.FillRectangle($lg, $rect)

# soft Mica-like glows
$br1 = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(30, 255, 255, 255))
$ex1 = [int](-$w * 0.35); $ey1 = [int](-$h * 0.20)
$ew1 = [int]($w * 1.20);  $eh1 = [int]($h * 0.65)
$g.FillEllipse($br1, $ex1, $ey1, $ew1, $eh1)
$br2 = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(18, 255, 255, 255))
$ex2 = [int]($w * 0.45); $ey2 = [int]($h * 0.55)
$ew2 = [int]($w * 0.90); $eh2 = [int]($h * 0.50)
$g.FillEllipse($br2, $ex2, $ey2, $ew2, $eh2)

# left accent stripe
$br3 = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(70, 255, 255, 255))
$g.FillRectangle($br3, 0, 0, 3, $h)

# rounded "brand card"
$cx = 30; $cy = 66; $cw = 104; $ch = 104; $rr = 22
$x2 = $cx + $cw - $rr; $y2 = $cy + $ch - $rr
$gp = [System.Drawing.Drawing2D.GraphicsPath]::new()
$gp.AddArc($cx, $cy, $rr, $rr, 180, 90)
$gp.AddArc($x2, $cy, $rr, $rr, 270, 90)
$gp.AddArc($x2, $y2, $rr, $rr, 0, 90)
$gp.AddArc($cx, $y2, $rr, $rr, 90, 90)
$gp.CloseFigure()
$card = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 255, 255, 255))
$g.FillPath($card, $gp)
$pen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(100, 255, 255, 255), [single]1.5)
$g.DrawPath($pen, $gp)

# "NEXT" wordmark
$f1 = [System.Drawing.Font]::new('Segoe UI', [single]21, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$cy2 = $cy - 2
$r1 = [System.Drawing.RectangleF]::new([single]$cx, [single]$cy2, [single]$cw, [single]$ch)
$g.DrawString('NEXT', $f1, $white, $r1, $sf)

# captions
$f2 = [System.Drawing.Font]::new('Segoe UI', [single]10, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$cap1 = [System.Drawing.RectangleF]::new([single]0, [single]190, [single]$w, [single]22)
$br4 = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(225, 255, 255, 255))
$g.DrawString('UnipusAI-Helper-NEXT', $f2, $br4, $cap1, $sf)
$f3 = [System.Drawing.Font]::new('Segoe UI', [single]9, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$cap2 = [System.Drawing.RectangleF]::new([single]0, [single]213, [single]$w, [single]18)
$br5 = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(160, 255, 255, 255))
$g.DrawString('Fluent Setup Experience', $f3, $br5, $cap2, $sf)

# accent rule
$lp = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(130, 255, 255, 255), [single]2)
$g.DrawLine($lp, 34, 284, 130, 284)

Save-Bmp $bmp 'WizardImage.bmp'
$g.Dispose(); $bmp.Dispose()

# ============ WizardSmallImage.bmp (55 x 55) ============
$sw = 55; $sh = 55
$sbmp = [System.Drawing.Bitmap]::new($sw, $sh, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
$sg = [System.Drawing.Graphics]::FromImage($sbmp)
$sg.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$sg.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$sp0 = [System.Drawing.Point]::new(0, 0)
$sp1 = [System.Drawing.Point]::new($sw, $sh)
$slg = [System.Drawing.Drawing2D.LinearGradientBrush]::new($sp0, $sp1, $c1, $c2)
$srect = [System.Drawing.Rectangle]::new(0, 0, $sw, $sh)
$sg.FillRectangle($slg, $srect)
$sr = 14
$sx2 = $sw - $sr; $sy2 = $sh - $sr
$sgp = [System.Drawing.Drawing2D.GraphicsPath]::new()
$sgp.AddArc(0, 0, $sr, $sr, 180, 90)
$sgp.AddArc($sx2, 0, $sr, $sr, 270, 90)
$sgp.AddArc($sx2, $sy2, $sr, $sr, 0, 90)
$sgp.AddArc(0, $sy2, $sr, $sr, 90, 90)
$sgp.CloseFigure()
$scard = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(45, 255, 255, 255))
$sg.FillPath($scard, $sgp)
$sf1 = [System.Drawing.Font]::new('Segoe UI', [single]30, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$sr1 = [System.Drawing.RectangleF]::new([single]0, [single]0, [single]$sw, [single]$sh)
$sg.DrawString('N', $sf1, $white, $sr1, $sf)
Save-Bmp $sbmp 'WizardSmallImage.bmp'
$sg.Dispose(); $sbmp.Dispose()

Write-Output 'IMAGES_OK'
