# 想象你没有拍摄平场的原因（虽然这没有好的理由，没有理由不拍摄平场！）。通过对上述代码进行小的修改，你可以

1. 检查平场文件夹是否包含任何文件或是否存在，
2. 调整脚本以跳过主平场的准备，
3. 调整光帧处理以跳过平场校准。

你需要做以下操作。

首先修改`light()`函数以接受一个参数来指示是否存在平场：

```python
def light(light_dir, process_dir, hasflats=True):
    cmd.cd(light_dir)
    cmd.convert('light', out=process_dir, fitseq=True)
    cmd.cd(process_dir)
    if hasflats:
        cmd.preprocess('light', dark='dark_stacked', flat='pp_flat_stacked', cfa=True, equalize_cfa=True, debayer=True)
    else:
        cmd.preprocess('light', dark='dark_stacked', cfa=True, debayer=True)
    cmd.register('pp_light')
    cmd.stack('r_pp_light', type='rej', sigma_low=3, sigma_high=3, norm='addscale', output_norm=True, out='../result')
    cmd.close()
```

然后修改主脚本以检查平场是否存在，并相应地调整处理流程：

```python
# 4. 准备主帧
flatsdir = workdir + '/flats'
hasflats = True
if not(os.path.isdir(flatsdir)) or (len(os.listdir(flatsdir)) == 0):  # 平场文件夹不包含任何文件或不存在
    hasflats = False

if hasflats:
    master_bias(workdir + '/biases', process_dir)
    master_flat(workdir + '/flats', process_dir)

master_dark(workdir + '/darks', process_dir)

# 5. 校准光帧，注册并叠加它们
light(workdir + '/lights', process_dir, hasflats)
```

这只是一个示例，你当然可以对暗场做同样的事情，使所有文件夹名称模块化，将其制作成一个带有I/O的模块，传递工作目录名称等。

## 使用Execute的处理示例

这段代码与上面的示例相同，只是它广泛使用了`Siril`类的`Execute`方法。`Execute('some command')`的工作方式与你在Siril命令行中键入`some command`完全相同。

```python
import sys
import os
from pysiril.siril import *

# ==============================================================================
# 使用Execute函数的OSC处理示例，不使用包装函数
# ==============================================================================

def master_bias(bias_dir, process_dir):
    app.Execute("cd " + bias_dir)
    app.Execute("convert bias -out=" + process_dir + " -fitseq")
    app.Execute("cd " + process_dir)
    app.Execute("stack bias rej 3 3  -nonorm")

def master_flat(flat_dir, process_dir):
    app.Execute("cd " + flat_dir + "\n"
                "convert flat -out=" + process_dir + " -fitseq" + "\n"
                "cd " + process_dir + "\n"
                "preprocess flat  -bias=bias_stacked" + "\n"
                "stack  pp_flat rej  3 3 -norm=mul")

def master_dark(dark_dir, process_dir):
    app.Execute(""" cd %s
                    convert dark -out=%s -fitseq
                    cd %s
                    stack dark rej 3 3 -nonorm """ % (dark_dir, process_dir, process_dir))

def light(light_dir, process_dir):
    app.Execute("cd " + light_dir)
    app.Execute("convert light -out=" + process_dir + " -fitseq")
    app.Execute("cd " + process_dir)
    app.Execute("preprocess light -dark=dark_stacked -flat=pp_flat_stacked -cfa -equalize-cfa -debayer")
    app.Execute("register pp_light")
    app.Execute("stack r_pp_light rej 3 3 -norm=addscale -output_norm -out=../result")
    app.Execute("close")

# ==============================================================================
workdir = "/home/barch/siril/work/TestSiril"
try:
    app.Open()
    process_dir = '../process'
    app.Execute("set16bits")
    app.Execute("setext fit")
    master_bias(workdir + '/biases', process_dir)
    master_flat(workdir + '/flats', process_dir)
    master_dark(workdir + '/darks', process_dir)
    light(workdir + '/lights', process_dir)
except Exception as e:
    print("\n**** ERROR *** " + str(e) + "\n")

app.Close()
del app
```

无论你选择使用`Execute`还是包装函数，都取决于你。你已经了解了用Python控制Siril的两种主要方式。

## 使用Addons

下面的示例展示了如何使用`Addons`类的一些功能。

```python
import sys
import os
from pysiril.siril import *
from pysiril.wrapper import *
from pysiril.addons import *

# ==============================================================================
# Addons函数示例
# ==============================================================================
app = Siril()
try:
    cmd = Wrapper(app)
    fct = Addons(app)

    # 创建一个序列文件
    workdir = "D:/_TraitAstro/20-SiriL/work/TestSiril"
    processdir = workdir + "/" + "xxxx"

    fct.CleanFolder(processdir, ext_list=[".cr2", ".seq"])

    fct.MkDirs(processdir)

    NbImage = fct.GetNbFiles(workdir + '/lights/*.CR2')
    print("CR2 number:", NbImage)

    number = fct.NumberImages(workdir + '/lights/*.CR2', processdir, "offsets", start=10, bOverwrite=True)

    if number == NbImage:
        fct.CreateSeqFile(processdir + "/toto.seq", number)
    else:
        print("error of images number:", number, "<>", NbImage)

except Exception as e:
    print("\n**** ERROR *** " + str(e) + "\n")

app.Close()
del app
```

## 返回值的函数

下面的示例展示了如何使用返回值的函数。它以`*.seq`文件作为输入，并写入一个包含`stat`命令返回值的csv文件。注意：由于Siril 0.99.8中添加了`seqstat`命令，此示例现已过时。尽管如此，它可以给你一些关于如何使用这些函数的想法。

```python
import os, sys
import re
import glob
from pysiril.siril import Siril
from pysiril.wrapper import Wrapper
from distutils.util import strtobool
import pandas as pd

def Run(inputfilename):
    folder, filename = os.path.split(inputfilename)
    fileroot, _ = os.path.splitext(filename)
    os.chdir(folder)

    with open(inputfilename) as f:
        lines = list(line for line in (l.strip() for l in f) if line)

    img = []
    for i, l in enumerate(lines):
        if l.startswith('S'):
            specline = l.split()
            lenseq = int(specline[3])

        if l.startswith('I'):
            tl = l.split()
            img.append(int(tl[1]))

    for ff in glob.iglob(fileroot + '*.f*'):
        _, fitext = os.path.splitext(ff)
        if not (fitext == '.seq'):
            break

    app = Siril(bStable=False)
    app.Open()
    cmd = Wrapper(app)

    res = []
    for i in range(lenseq):
        fitfile = '{0:s}{1:05d}{2:s}'.format(fileroot, img[i], fitext)
        cmd.load(fitfile)
        _, stats = cmd.stat()
        for j in range(len(stats)):
            stats[j]['file'] = fitfile
            stats[j]['image#'] = img[i]
            res.append(stats[j])
    app.Close()
    del app

    data = pd.DataFrame.from_dict(res)
    data.set_index(['file', 'image#', 'layer'], inplace=True)
    data.reset_index(inplace=True)
    data.to_csv(fileroot + 'stats.csv', index=False)

if __name__ == "__main__":
    args = []
    kwargs = {}
    for a in sys.argv[1:]:
        if '=' in a:
            f, v = a.split('=')
            kwargs[f] = v
        else:
            args.append(a)
    Run(*tuple(args), **kwargs)
```

要运行它：

1. 将此代码复制/粘贴到你最喜欢的编辑器中，
2. 将其保存为`seqstat.py`，
3. 在shell中键入：

   ```bash
   python seqstat.py "C:\Users\myusername\Pictures\astro\myseqfile_.seq"
   ```

   这将在同一文件夹中保存`myseqfile_stats.csv`。

## 将单图像命令应用于序列

最后一个示例是[此处](https://siril.org/tutorials/scripts/)所示的shell脚本的Python等效版本。它使用了上面详细介绍的所有概念。只需将下面的代码复制并保存到名为`genseqscript.py`的文件中。

```python
# 用法
#######
# genseqscript.py command seqname [prefix ext]
# 示例：
###########
#
# 对C:\MyImages\r_pp_light_.seq中的所有图像应用中值滤波器，扩展名为“fit”，并以“med_”前缀保存
# python genseqscript.py "fmedian 5 1" "C:\MyImages\r_pp_light_.seq" med_ fit
#
# 对当前文件夹中的pp_light_.seq中的所有图像应用90度旋转（不裁剪）
# python genseqscript.py "rotate 90 -nocrop" pp_light_ rot90_

# 用户设置
# command: 要应用于序列中每个图像的命令。如果有多个单词，请用双引号括起来
# seqname: 序列的名称，可以是完整路径或当前目录中的序列名称（带或不带.seq扩展名）。如果路径中有空格，请用双引号括起来
# prefix: （可选）要添加到处理文件名称的前缀，默认：""
# ext: （可选）选择的FITS扩展名，默认：fits（也可以是fit或fts）
import os, sys
from pysiril.siril import Siril
from pysiril.wrapper import Wrapper
from pysiril.addons import Addons

def Run(command, seqname, prefix='', ext='fits'):
    print('Command to be run: {0:s}'.format(command))
    print('prefix: {0:s}'.format(prefix))
    print('FITS extension: {0:s}'.format(ext))

    if os.path.isabs(seqname):
        currdir, seqname = os.path.split(seqname)
    else:
        currdir = os.getcwd()

    seqname, seqext = os.path.splitext(seqname)
    if len(seqext) == 0:
        seqext = '.seq'

    print('Working directory: {0:s}'.format(currdir))
    print('Sequence to be processed: {0:s}{1:s}'.format(seqname, seqext))

    if not (os.path.isfile(os.path.join(currdir, seqname + seqext))):
        print('The specified sequence does not exist - aborting')
        sys.exit()

    print('Starting PySiril')
    app = Siril(R'C:\Program Files\SiriL\bin\siril-cli.exe')
    AO = Addons(app)
    cmd = Wrapper(app)

    print('Starting Siril')
    try:
        app.Open()
        seqfile = AO.GetSeqFile(os.path.join(currdir, seqname + seqext))
        app.Execute('setext {:s}'.format(ext))
        app.Execute('cd "{:s}"'.format(currdir))
        for im in seqfile['images']:
            currframenb = im['filenum']
            currframe = '{0:s}{1:05d}.{2:s}'.format(seqname, currframenb, ext)
            if not (os.path.isfile(os.path.join(currdir, currframe))):
                print('First file {0:s} does not exist... check if the .seq file is valid or the selected FITS extension ("{1:s}" defined here) matches your files - aborting'.format(currframe, ext))
                sys.exit()
            print('processing file: {0:s}'.format(currframe))
            savename = prefix + currframe
            cmd.load(currframe)
            app.Execute(command)
            cmd.save(savename)
        app.Close()
        del app
    except Exception as e:
        print("\n**** ERROR *** " + str(e) + "\n")

if __name__ == "__main__":
    args = []
    kwargs = {}
    for a in sys.argv[1:]:
        if '=' in a:
            f, v = a.split('=', 1)
            kwargs[f] = v
        else:
            args.append(a)
    Run(*tuple(args), **kwargs)
```
