# 使用bash或DOS进行高级Siril脚本编写

对于命令行爱好者来说，Siril允许您将其脚本（一系列简单的Siril命令）集成到更强大的shell脚本（bash或dos）中，这些脚本可以管理变量。在本教程中，我们将看到如何在UNIX类型的平台以及Microsoft Windows上创建此类脚本。我们将展示的第一个示例是将2x2 bin图像重新采样为1x1 bin，使用siril resample命令将其大小乘以2。之后的一个更复杂的示例展示了如何将仅适用于单图像的命令应用于序列中的所有图像。

## 重新采样图像

### UNIX

初步步骤是创建文件并使其可执行：

```bash
touch resample
chmod a+x resample
```

编辑文件并复制以下文本：

```bash
#!/bin/bash
#
#  重新采样文件
#  用于将bin 2x2重新采样为1x1
#  对于lrgb有用，其中l为1x1，rgb为2x2
#
version=$(siril --version |awk '{print $2}')
ext=fits

siril-cli -i ~/.siril/siril.cfg -s - <<ENDSIRIL >/dev/null 2>&1
requires $version
setext $ext
load $1
resample 2.0
save $1
close
ENDSIRIL
```

保存文件然后关闭它，然后只需通过键入以下命令运行脚本：

```bash
./resample 文件名
```

或者，如果文件名中包含模式2x2：

```bash
for i in $(/bin/ls *.fits |grep 2x2); do ./resample $i; done
```

**注意：** 对于MacOS系统，脚本的工作方式相同，只需将siril路径更新为类似`/Applications/SiriL.app/Contents/MacOS/siril`的内容。

### Microsoft Windows (cmd)

使用以下命令行创建一个空文件：

```cmd
copy NUL resample.bat
```

或当然通过UI。

编辑文件并复制以下文本：

```cmd
echo OFF
FOR /F "tokens=2 " %%g IN ('siril --version') do (SET version=%%g)
set ext=fits

(
echo requires %version%
echo setext %ext%
echo load %1
echo resample 2.0
echo save %1
echo close
) | "C:\Program Files\SiriL\bin\siril-cli.exe" -s - >nul 2>&1

pause
```

保存文件然后关闭它。您现在可以通过将图片拖到其图标上或键入以下命令来运行脚本：

```cmd
resample.bat 文件名
```

## 将单图像命令应用于序列

### UNIX

如上所示创建一个可执行文件并复制以下内容：

```bash
#!/bin/bash

# 用法
#######
# ./genseqscript.sh 命令 序列名 [前缀 扩展名]
# 示例：
###########
#
# 对/Images/siril/process/r_pp_light_.seq中的所有图像应用中值滤波器，扩展名为“fit”，并以“med_”前缀保存
# ./genseqscript.sh "fmedian 5 1" "/Images/siril/process/r_pp_light_.seq" med_ fit
#
# 对当前文件夹中的pp_light_.seq中的所有图像应用90度旋转（不裁剪）
# ./genseqscript.sh "rotate 90 -nocrop" "pp_light_" rot90_

# 用户设置
# 命令：要应用于序列中每个图像的命令
# 序列名：序列的名称，可以是完整路径或当前目录中的序列名称（带或不带.seq扩展名）
# 前缀：（可选）要添加到处理文件名称的前缀，默认：""
# 扩展名：（可选）选择的FITS扩展名，默认：fits（也可以是fit或fts）

# 默认值
prefix=""
ext=fits


# 用户命令行输入
if [[ $# -lt 2 ]]; then
    echo "非法参数数量 - 您应至少传递命令和序列名称" >&2
    exit 1
fi
if [ ! -z "$1" ]; then command="$1"; fi
if [ ! -z "$2" ]; then seqname="$2"; fi
if [ ! -z "$3" ]; then prefix="$3"; fi
if [ ! -z "$4" ]; then ext="$4"; fi

printf "要运行的命令：%s\n" "$command"
printf "序列名称：%s\n" $seqname
printf "前缀：%s\n" $prefix
printf "FITS扩展名：%s\n" $ext

currdir=$(dirname "$seqname")
seqname=$(basename "$seqname")
seqext=".seq"


if [ "$currdir" = "." ]; then currdir=$(pwd); fi
if [ "${seqname: -4}" = $seqext ]; then seqname="${seqname%.*}"; fi
fullseqname="$currdir"/"$seqname"$seqext

printf "工作目录：%s\n" "$currdir"
printf "要处理的序列：%s%s\n" "$seqname" $seqext

[[ -f "$currdir"/"$seqname"$seqext ]] || { echo "指定的序列不存在 - 中止"; exit 1; }

# 获取siril版本
version=$(siril-cli --version |awk '{print $2}')

while read line
do
  if [[ "$line" =~ ^I.* ]]; then
    spec=($line)
    currframenb=${spec[1]}
    currframe=$(printf "$seqname%05d.$ext" $((currframenb)))
    savename=$prefix"$currframe"
    # 检查第一帧是否存在，否则中断
    [[ -f "$currdir"/"$currframe" ]] || { printf "第一文件 %s 不存在... 检查.seq文件是否有效或选择的FITS扩展名（此处定义为'%s'）是否与您的文件匹配 - 中止\n" "$currframe" $ext; exit 1; }
    
    printf "正在处理文件：%s\n" "$currframe"
    siril-cli -s - <<ENDSIRIL >log 2>&1
requires $version
setext $ext
cd "$currdir"
load "$currframe"
$command
save "$savename"
ENDSIRIL
  fi
done < "$currdir"/"$seqname"$seqext
```

将其保存为`genseqscript.sh`

只需通过键入以下命令运行脚本：

```bash
./genseqscript.sh "fmedian 5 1" "/Images/siril/process/r_pp_light_.seq" med_ fit
```

这将应用一个中值滤波器到`/Images/siril/process/r_pp_light_.seq`中的所有图像，扩展名为“fit”，并以“med_”前缀保存。当然，您可以传递任何（有效的）命令。浏览此页面以了解更多信息。还要首先检查您希望应用的转换是否已经存在seq等效项，因为它将由于并行化而执行得更快。

### Microsoft Windows (Powershell)

同样可以在Microsoft Windows上使用Powershell（而不是如上所示的cmd）完成。创建文件`genseqscript.ps1`并复制以下内容：

```powershell
# 用法
#######
# .\genseqscript.ps1 命令 序列名 [前缀 扩展名]
# 示例：
###########
#
# 对C:\MyImages\r_pp_light_.seq中的所有图像应用中值滤波器，扩展名为“fit”，并以“med_”前缀保存
# .\genseqscript.ps1 "fmedian 5 1" "C:\MyImages\r_pp_light_.seq" med_ fit
#
# 对当前文件夹中的pp_light_.seq中的所有图像应用90度旋转（不裁剪）
# .\genseqscript.ps1 "rotate 90 -nocrop" pp_light_ rot90_

# 用户设置
# 命令：要应用于序列中每个图像的命令。如果有多个单词，请用双引号括起来
# 序列名：序列的名称，可以是完整路径或当前目录中的序列名称（带或不带.seq扩展名）。如果路径中有空格，请用双引号括起来
# 前缀：（可选）要添加到处理文件名称的前缀，默认：""
# 扩展名：（可选）选择的FITS扩展名，默认：fits（也可以是fit或fts）

# 用户命令行输入（如果有）
param ($command,$seqname,$prefix="",$ext="fits" )
"要运行的命令：{0:s}" -f $command
"前缀：{0:s}" -f $prefix
"FITS扩展名：{0:s}" -f $ext

If (Split-Path -Path $seqname -IsAbsolute) {
    $currdir = Split-Path -Path $seqname
    $seqname = Split-Path -Path $seqname -Leaf
}
Else {
    $currdir = (Get-Location).path
}

$seqext = [IO.Path]::GetExtension($seqname)
If ($seqext.Length -eq 0){
    $seqext = '.seq'
}
Else {
    $seqname = [IO.Path]::GetFileNameWithoutExtension($seqname)
}

"工作目录：{0:s}" -f $currdir
"要处理的序列：{0:s}{1:s}" -f $seqname,$seqext
If (-Not (Test-Path -Path $currdir\$seqname$seqext -PathType Leaf )){
    "指定的序列不存在 - 中止"
    Exit
}

# siril-cli的路径
$sirilcliexe="C:\Program Files\SiriL\bin\siril-cli.exe"

# 获取siril版本
$version=($(& $sirilcliexe --version) -split ' ')[-1]
$log="{0:s}\log.txt"-f $currdir

Get-Content $currdir\$seqname$seqext | Select-String -Pattern '^I ' | ForEach-Object {

  $currframenb=[int]($_ -split ' ')[1]
  $currframe="{0:s}{1:00000}.{2:s}" -f "$seqname",$currframenb,$ext
  # 检查第一帧是否存在，否则中断
  If (-Not (Test-Path -Path "$currdir\$currframe" -PathType Leaf )){
    "第一文件 {0:s} 不存在... 检查.seq文件是否有效或选择的FITS扩展名（此处定义为'{1:s}'）是否与您的文件匹配 - 中止" -f $currframe,$ext
    Exit
  }
  "正在处理文件：{0:s}" -f "$currframe"
  $savename=$prefix+"$currframe"

  @"
requires $version
setext $ext
cd "$currdir"
load "$currframe"
$command
save "$savename"
"@ | & $sirilcliexe -s - >$log 2>&1
}
```

只需在powershell控制台中键入以下命令运行脚本：

```powershell
.\genseqscript.ps1 "fmedian 5 1" "C:\MyImages\r_pp_light_.seq" med_ fit
```

这将应用一个中值滤波器到`C:\MyImages\r_pp_light_.seq`中的所有图像，扩展名为“fit”，并以“med_”前缀保存。当然，您可以传递任何（有效的）命令。浏览此页面以了解更多信息。还要首先检查您希望应用的转换是否已经存在seq等效项，因为它将由于并行化而执行得更快。

## 结论

这些示例表明，可以使用shell脚本的强大功能与Siril结合，编写图像处理步骤的每一步。唯一的限制是您的想象力。
