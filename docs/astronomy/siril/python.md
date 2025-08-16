
# Siril Python Scripting: The Definitive Guide

## Part 1: Introduction and Core Concepts

### 1.1 The Power of Python in Siril: Beyond Legacy Scripts

The introduction of a Python scripting interface in Siril version 1.4 represents the most significant evolution in the software's automation capabilities. Prior to this, automation was handled through Siril Script Files (`.ssf`), which provided a powerful but fundamentally limited method for batch processing. These legacy scripts operate as a linear, non-configurable sequence of commands, executing a predefined workflow from start to finish. While effective for standardizing repetitive tasks, this approach lacked the flexibility to adapt to varying conditions, handle complex logic, or integrate with external tools.

The Python interface fundamentally changes this paradigm. It transforms Siril from a tool that can be automated into a fully programmable image processing engine. By leveraging the full power of the Python language, users can now implement dynamic and intelligent workflows that were previously impossible. Key advantages include:

* **Conditional Logic**: Scripts can make decisions based on image properties or user input using `if`, `else`, and `elif` statements. For example, a script can check if a flats directory exists and skip the flat-fielding step if it is empty.
* **Loops and Iteration**: Repetitive tasks can be managed with `for` and `while` loops, allowing scripts to process an arbitrary number of files, iterate through sequence frames, or perform operations on a list of detected stars.
* **Variables and State Management**: Data can be stored in variables, passed between functions, and used to dynamically configure Siril commands. This allows for the creation of responsive scripts where, for instance, a calculated value from one processing step (like the average FWHM of stars) can determine the parameters of a subsequent step (like deconvolution).
* **Functions and Modularity**: Complex workflows can be broken down into reusable functions, making scripts cleaner, easier to read, and simpler to maintain.
* **Integration with External Libraries**: Perhaps the most powerful feature is the ability to seamlessly integrate with the vast scientific Python ecosystem. Libraries such as Astropy, NumPy, SciPy, and Photutils can be used directly within a Siril script, opening up limitless possibilities for custom analysis, specialized algorithms, and advanced data visualization.

This transition marks a "huge step forward," moving beyond simple command sequences to enable true algorithmic control over the image processing pipeline.

### 1.2 Understanding the Interfaces: sirilpy vs. pysiril (A Critical Distinction)

The Siril automation ecosystem includes two distinct Python libraries: `sirilpy` and `pysiril`. Understanding the purpose and design of each is critical for selecting the correct tool for a given task. While both allow for the execution of Siril commands via Python, they operate on fundamentally different principles and are designed for different use cases.

* **sirilpy: The Internal Scripting Interface**  
  `sirilpy` is the primary focus of this guide and represents the modern, integrated scripting solution introduced in Siril 1.4. It functions as an internal interface, meaning scripts using `sirilpy` are executed from within a running instance of the Siril application. A script establishes a connection to the Siril process it is running in, allowing it to interact directly with the application's current state, including the loaded image or sequence, user interface elements, and internal data structures.

  **Primary Use Cases for sirilpy:**
  * Developing complex, interactive tools that appear in the Siril "Scripts" menu.
  * Creating custom processing steps that require access to the currently loaded image data for analysis and modification.
  * Building scripts that provide real-time feedback to the user through Siril's log, progress bar, or message boxes.
  * Extending the Siril GUI with new capabilities that leverage external Python libraries for analysis and visualization.

* **pysiril: The External Automation Library**  
  `pysiril` is an external library designed to control Siril as a separate, headless process. Scripts using `pysiril` are standalone Python programs that launch, command, and terminate an instance of Siril's command-line interface (`siril-cli`). This model is ideal for non-interactive, large-scale automation where no graphical user interface is required. The external program Sirilic, which provides a graphical front-end for complex batch processing, is a prime example of an application built upon `pysiril`.

  **Primary Use Cases for pysiril:**
  * Automating the processing of large datasets on a remote server or in a cloud environment.
  * Integrating Siril's processing capabilities into a larger, non-interactive scientific pipeline.
  * Building custom applications or services that use Siril as a backend processing engine.

The existence of these two separate libraries is not a redundancy but a reflection of a mature and well-considered automation strategy. It acknowledges that users have distinct automation needs. The `sirilpy` interface serves the user who wants to enhance their interactive workflow within the Siril application, while `pysiril` serves the user who wants to use Siril as a powerful tool in a larger, non-interactive system. This clear separation of concerns allows each library to be optimized for its specific purpose. A simple way to remember the distinction is: **"sirilpy to extend Siril with Python, pysiril to extend your Python program with Siril"**.

## Part 2: Installation and Environment Setup

### 2.1 System Prerequisites

To utilize the Python scripting interface, a few prerequisites must be met. These ensure that Siril can correctly establish and manage its dedicated scripting environment.

1. **Siril Version**: Python scripting is a feature introduced in version 1.4.0. Therefore, an installation of Siril 1.4.0 or newer is mandatory. It is always recommended to use the latest stable release to benefit from bug fixes and API improvements.
2. **Python Installation**: Siril requires a functional system-level installation of Python version 3.9 or higher. This base installation is used by Siril to create its own isolated virtual environment. The pre-built binary packages of Siril for Windows, macOS, and Linux typically bundle the necessary Python components. However, if compiling Siril from source or using certain system package managers, it is essential to ensure that the following Python modules are available:
   * `python3-venv`: The standard library module for creating virtual environments.
   * `python3-pip`: The package installer for Python, used to manage libraries within the virtual environment.
   * `python3-tk`: The Tkinter toolkit, which is required for scripts that implement graphical user interfaces (GUIs).

### 2.2 Siril's Managed Python Environment (The venv)

A core feature of Siril's Python integration is its use of a managed, self-contained virtual environment (venv). When a Python script is run for the first time, Siril automatically creates this dedicated environment, typically located within its user configuration directory. This approach provides several significant advantages for both users and script developers.

The primary purpose of the managed venv is to ensure a consistent and predictable execution environment across all platforms and user setups. By isolating the scripting environment from the user's system-level Python installation, Siril prevents potential conflicts arising from different library versions or Python configurations. This design choice dramatically increases the reliability of scripts, especially those shared through the official Siril Scripts repository, as they are executed in a standardized sandbox.

This architecture represents a deliberate trade-off, prioritizing robustness and ease of use for the majority of users over the advanced flexibility that some power users might prefer. Instead of requiring each user to manage their own complex environments (e.g., using conda or manual venv creation), which would create a significant support burden, Siril provides a system that "just works" out of the box. All Python scripts executed within Siril share this single venv. This shared nature has an important implication for dependency management: scripts should avoid specifying restrictive version constraints (e.g., `astropy==5.0.4`) as this could create conflicts with other scripts that require a different version of the same library. Best practice, as will be detailed later, is to use open-ended minimum version constraints (e.g., `astropy>=5.0`).

### 2.3 Establishing a Connection

Every `sirilpy` script begins with the same fundamental steps: importing the library and establishing a connection with the running Siril instance. The library can be imported using `import sirilpy`. For convenience and to follow common Python conventions, it is often aliased as `s`: `import sirilpy as s`.

Once imported, the connection is managed through the `SirilInterface` class. An instance of this class is created, and its `connect()` method is called to establish the communication pipe with Siril. Because the connection can fail if Siril is not in a ready state, this operation should always be wrapped in a `try...except` block to gracefully handle a `SirilConnectionError`.

The following code provides the standard boilerplate for initializing any `sirilpy` script:

```python
# English: Basic connection setup
import sirilpy as s

# Instantiate the interface
siril = s.SirilInterface()

try:
   # Establish the connection to the running Siril instance
   siril.connect()
   siril.log("Python script connected successfully!")
except s.SirilConnectionError as e:
   # Use Siril's logging for errors if connection fails
   print(f"Connection failed: {e}")
```

```python
# Chinese (简体中文): 基本连接设置
import sirilpy as s

# 实例化接口
siril = s.SirilInterface()

try:
   # 建立与正在运行的 Siril 实例的连接
   siril.connect()
   siril.log("Python 脚本连接成功！")
except s.SirilConnectionError as e:
   # 如果连接失败，使用标准打印输出错误
   print(f"连接失败: {e}")
```

The use of `siril.log()` sends a message directly to the Siril console, which is the preferred method for providing feedback to the user once a connection is established.

### 2.4 Managing External Libraries with ensure_installed()

While the `sirilpy` module and its dependency, NumPy, are automatically available in Siril's venv, most advanced scripts will require additional third-party libraries like astropy, photutils, or matplotlib. To simplify the management of these dependencies for the end-user, `sirilpy` provides a crucial utility function: `ensure_installed()`.

This function checks if a specified package is installed in Siril's venv. If the package is not found, `ensure_installed()` will automatically attempt to install it using pip. This process is transparent to the user, who simply runs the script. A message is printed to the Siril log indicating that a one-time installation is in progress. On subsequent runs, the check is nearly instantaneous as the package is already present.

This utility is the cornerstone of writing portable and user-friendly scripts. It removes the burden on the user to manually install dependencies, which is a common point of failure in scientific computing workflows.

The correct usage pattern is to call `ensure_installed()` for each required package before its corresponding import statement. To avoid version conflicts in the shared venv, it is strongly recommended to specify only minimum version requirements using the `>=` operator.

```python
# English: Example of managing dependencies
import sirilpy as s

# --- Connect to Siril (from previous example) ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   # Handle connection error
   quit()

try:
   # Ensure astropy version 6.0 or newer is installed
   s.ensure_installed("astropy", version_constraints=">=6.0")
   # Ensure photutils is installed
   s.ensure_installed("photutils")

   # Now, it is safe to import the libraries
   import astropy
   from astropy.io import fits
   import photutils

   siril.log("All required libraries are present.")

except (ImportError, ModuleNotFoundError) as e:
   siril.error_messagebox(f"A required library could not be installed or imported: {e}")
except Exception as e:
   siril.error_messagebox(f"An unexpected error occurred during setup: {e}")
```

```python
# Chinese (简体中文): 依赖管理示例
import sirilpy as s

# --- 连接到 Siril (来自前一个示例) ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   # 处理连接错误
   quit()

try:
   # 确保安装了 astropy 6.0 或更高版本
   s.ensure_installed("astropy", version_constraints=">=6.0")
   # 确保安装了 photutils
   s.ensure_installed("photutils")

   # 现在，可以安全地导入这些库
   import astropy
   from astropy.io import fits
   import photutils

   siril.log("所有必需的库都已存在。")

except (ImportError, ModuleNotFoundError) as e:
   siril.error_messagebox(f"无法安装或导入所需的库: {e}")
except Exception as e:
   siril.error_messagebox(f"设置过程中发生意外错误: {e}")
```

This robust pattern ensures that the script's dependencies are met automatically, providing a smooth experience for the user and making the script more portable.

## Part 3: The sirilpy API: A Complete Reference

This section provides a comprehensive reference for the `sirilpy` Application Programming Interface (API). The core of the interface is the `SirilInterface` class, which provides methods for commanding Siril, retrieving data, and interacting with the user interface. The API is designed to be both powerful and intuitive, giving scripts deep access to Siril's internal state and processing capabilities.

### 3.1 The SirilInterface Class and Connection Management

These are the foundational methods for initializing and managing the script's connection to the Siril application.

* **SirilInterface()**
  * *Description*: The constructor for the main interface class. This object is the entry point for all interactions with Siril.
  * *Signature*: `SirilInterface()`
  * *Returns*: An instance of the `SirilInterface` class.

* **connect()**
  * *Description*: Establishes the communication pipe or socket with the running Siril instance. This method must be called before any other interaction with Siril.
  * *Signature*: `connect()`
  * *Returns*: `bool` - True on success.
  * *Raises*: `SirilConnectionError` if the connection cannot be established.

* **disconnect()**
  * *Description*: Closes the connection to Siril. This is typically not needed, as the connection is closed automatically when the script terminates.
  * *Signature*: `disconnect()`
  * *Raises*: `SirilConnectionError` if the connection cannot be closed properly.

* **is_cli()**
  * *Description*: Checks if the script is running in a headless (`siril-cli`) or GUI instance of Siril.
  * *Signature*: `is_cli()`
  * *Returns*: `bool` - True if running in command-line mode, False otherwise.

### 3.2 Command Execution: The cmd() Workhorse

The `cmd()` method is the most frequently used function in `sirilpy`. It is the universal mechanism for executing any of Siril's internal commands, from loading files to performing complex processing tasks.

* **cmd(*args)**
  * *Description*: Sends a command string and its arguments to Siril for execution. The command and each argument should be passed as separate string arguments to the function.
  * *Signature*: `cmd(*args: str)`
  * *Parameters*:
    * `*args` (`str`): A variable number of string arguments. The first argument is the command name, and subsequent arguments are its parameters.
  * *Returns*: `None`.
  * *Raises*:
    * `CommandError`: If the Siril command returns an error status. This is the most common exception and indicates a problem with the command's execution (e.g., file not found, invalid parameter).
    * `DataError`: If an invalid response is received from Siril.
    * `SirilError`: For other generic errors.
  * *Example*:

```python
# English: Using the cmd() function
# Set the working directory
siril.cmd("cd", "/path/to/my/data")
# Pre-process a sequence named 'light'
siril.cmd("preprocess", "light", "-dark=darks_stacked", "-flat=flats_stacked")
# Stack the registered sequence with dynamic parameters
sigma_val = 3.0
siril.cmd("stack", "r_pp_light", "rej", f"{sigma_val}", f"{sigma_val}", "-norm=addscale")
```

```python
# Chinese (简体中文): 使用 cmd() 函数
# 设置工作目录
siril.cmd("cd", "/path/to/my/data")
# 预处理名为 'light' 的序列
siril.cmd("preprocess", "light", "-dark=darks_stacked", "-flat=flats_stacked")
# 使用动态参数叠加已对齐的序列
sigma_val = 3.0
siril.cmd("stack", "r_pp_light", "rej", f"{sigma_val}", f"{sigma_val}", "-norm=addscale")
```

### 3.3 Image Data Handling (Single Images)

These methods provide access to the pixel data and metadata of a single image currently loaded in Siril.

* **is_image_loaded()**
  * *Description*: Checks if a single image (not a sequence) is currently loaded.
  * *Signature*: `is_image_loaded()`
  * *Returns*: `bool` - True if an image is loaded.

* **get_image(with_pixels=True, preview=False)**
  * *Description*: Retrieves the currently loaded image as an `FFit` data object. This object contains all metadata and, optionally, the pixel data.
  * *Signature*: `get_image(with_pixels: bool = True, preview: bool = False)`
  * *Parameters*:
    * `with_pixels` (`bool`): If True (default), the pixel data is included as a NumPy array in the `.data` attribute of the returned object.
    * `preview` (`bool`): If True, returns an 8-bit, auto-stretched preview image instead of the full-bit-depth scientific data.
  * *Returns*: An `FFit` object containing the image data and metadata.
  * *Raises*: `NoImageError` if no image is loaded.

* **get_image_pixeldata(shape=None, preview=False)**
  * *Description*: A more direct method to retrieve only the pixel data of the current image as a NumPy array.
  * *Signature*: `get_image_pixeldata(shape: list = None, preview: bool = False)`
  * *Parameters*:
    * `shape` (`list`): An optional list `[x, y, w, h]` to retrieve data from a specific rectangular region.
    * `preview` (`bool`): If True, returns an 8-bit preview.
  * *Returns*: `numpy.ndarray` containing the pixel data.
  * *Raises*: `NoImageError` if no image is loaded.

* **set_image_pixeldata(image_data)**
  * *Description*: Updates the currently loaded image in Siril with new pixel data from a NumPy array. This is the primary method for modifying image data from a script. This function must be called within an `image_lock()` context.
  * *Signature*: `set_image_pixeldata(image_data: numpy.ndarray)`
  * *Parameters*:
    * `image_data` (`numpy.ndarray`): A 2D (monochrome) or 3D (RGB) NumPy array with dtype of `np.float32` or `np.uint16`.
  * *Returns*: `bool` - True on success.
  * *Raises*: `NoImageError`, `ValueError` (for invalid array shape/type).

* **image_lock()**
  * *Description*: A context manager (`with` statement) that claims exclusive access to the image processing thread. This is mandatory for any read-modify-write operation on pixel data to prevent race conditions and data corruption. Siril is a multithreaded application, and without this lock, the GUI or another process could attempt to access the image buffer while the Python script is modifying it. The lock ensures that the sequence of getting pixel data, processing it, and setting it back is atomic and safe.
  * *Signature*: `with siril.image_lock():...`
  * *Raises*: `ProcessingThreadBusyError`, `ImageDialogOpenError`.
  * *Example*:

```python
# English: Correctly modifying image data using image_lock
try:
   with siril.image_lock():
       # This block has exclusive access to the image
       img_data = siril.get_image_pixeldata()
       # Perform some operation, e.g., increase brightness
       img_data *= 1.5
       siril.set_image_pixeldata(img_data)
       siril.cmd("autostretch") # Update the display
except s.ProcessingThreadBusyError:
   siril.error_messagebox("Could not get a lock on the image. Is another process running?")
except s.NoImageError:
   siril.error_messagebox("Please load an image first.")
```

```python
# Chinese (简体中文): 使用 image_lock 正确修改图像数据
try:
   with siril.image_lock():
       # 此代码块独占对图像的访问权限
       img_data = siril.get_image_pixeldata()
       # 执行某些操作，例如增加亮度
       img_data *= 1.5
       siril.set_image_pixeldata(img_data)
       siril.cmd("autostretch") # 更新显示
except s.ProcessingThreadBusyError:
   siril.error_messagebox("无法锁定图像。是否有其他进程正在运行？")
except s.NoImageError:
   siril.error_messagebox("请先加载图像。")
```

### 3.4 Sequence Data Handling

These methods are analogous to the single-image functions but operate on image sequences.

* **is_sequence_loaded()**
  * *Description*: Checks if a sequence is currently loaded.
  * *Signature*: `is_sequence_loaded()`
  * *Returns*: `bool` - True if a sequence is loaded.

* **get_seq()**
  * *Description*: Retrieves the metadata for the entire loaded sequence as a `Sequence` data object. This object contains information like the number of frames, dimensions, and lists of per-frame metadata, but not the pixel data itself.
  * *Signature*: `get_seq()`
  * *Returns*: A `Sequence` object.
  * *Raises*: `NoSequenceError` if no sequence is loaded.

* **get_seq_frame(frame, with_pixels=True)**
  * *Description*: Retrieves a single frame from the sequence as an `FFit` object, similar to `get_image()`.
  * *Signature*: `get_seq_frame(frame: int, with_pixels: bool = True)`
  * *Parameters*:
    * `frame` (`int`): The zero-based index of the frame to retrieve.
  * *Returns*: An `FFit` object for the specified frame.
  * *Raises*: `NoSequenceError`.

* **get_seq_frame_pixeldata(frame)**
  * *Description*: Retrieves only the pixel data for a specific frame as a NumPy array.
  * *Signature*: `get_seq_frame_pixeldata(frame: int)`
  * *Returns*: `numpy.ndarray`.
  * *Raises*: `NoSequenceError`.

* **set_seq_frame_pixeldata(index, image_data)**
  * *Description*: Updates a specific frame in the sequence with new pixel data. Requires an `image_lock`.
  * *Signature*: `set_seq_frame_pixeldata(index: int, image_data: numpy.ndarray)`
  * *Returns*: `bool` - True on success.
  * *Raises*: `NoSequenceError`.

* **set_seq_frame_incl(index, incl)**
  * *Description*: Sets whether a frame is included or excluded from processing (the checkbox in the "Image List" tab).
  * *Signature*: `set_seq_frame_incl(index: int, incl: bool)`
  * *Parameters*:
    * `index` (`int`): The zero-based index of the frame.
    * `incl` (`bool`): True to include the frame, False to exclude it.
  * *Raises*: `NoSequenceError`.

### 3.5 Metadata, Headers, and Scientific Data

This group of functions provides access to the rich scientific data associated with astronomical images.

* `get_image_filename()`: Returns the filename of the currently loaded image as a `str`.
* `get_image_fits_header()`: Returns the full FITS header of the current image as a single `str`.
* `get_image_keywords()`: Returns an `FKeywords` object containing parsed values of common FITS keywords (e.g., exposure time, camera temperature).
* `get_image_stats(channel)`: Returns an `ImageStats` object with detailed statistics (mean, median, std dev, etc.) for the specified channel (0 for Red/Mono, 1 for Green, 2 for Blue).
* `get_selection_stats()`: Returns an `ImageStats` object for the current rectangular selection in the GUI.
* `get_image_stars()`: After running `findstar` or a similar command, this returns a list of `PSFStar` objects, each containing detailed fitted parameters (position, FWHM, magnitude, etc.) for a detected star.
* `pix2radec(x, y)`: For a plate-solved image, converts pixel coordinates (x, y) to celestial coordinates (Right Ascension, Declination). Returns a tuple of two floats.
* `radec2pix(ra, dec)`: For a plate-solved image, converts celestial coordinates (ra, dec) to pixel coordinates. Returns a tuple of two floats.

### 3.6 User Interface and Progress Reporting

These methods allow a script to communicate with the user through the Siril GUI.

* `log(message, color=LogColor.DEFAULT)`: Prints a message to the Siril console log. The color can be specified using the `LogColor` enum (e.g., `s.LogColor.GREEN`, `s.LogColor.RED`).
* `info_messagebox(message)`: Displays a non-modal informational message box.
* `warning_messagebox(message)`: Displays a non-modal warning message box.
* `error_messagebox(message)`: Displays a non-modal error message box.
* `confirm_messagebox(title, message, confirm_label)`: Displays a modal confirmation dialog that pauses the script. Returns True if the user clicks the confirmation button, False otherwise.
* `update_progress(message, progress)`: Updates Siril's main progress bar. `message` is the text to display, and `progress` is a float between 0.0 and 1.0.
* `reset_progress()`: Resets and hides the progress bar.

### 3.7 Overlays and Plotting

These functions enable scripts to draw on the image display and create plots.

* `overlay_add_polygon(polygon)`: Adds a `Polygon` object to be drawn on the image overlay.
* `overlay_clear_polygons()`: Removes all script-drawn polygons from the overlay.
* `overlay_draw_polygon()`: Enters an interactive mode where the user can draw a polygon on the image, which is then returned to the script.
* `xy_plot(plot_data)`: Displays Siril's native plotting tool with data provided in a `PlotData` object. This is useful for quickly visualizing results like light curves or profiles.

### 3.8 Data Models and Enums

The `sirilpy` API uses a set of custom data classes to represent Siril's internal C structures in a Python-friendly way. When a script requests data (e.g., with `get_image()`), the API returns an instance of one of these classes. Understanding their structure is key to accessing the returned data.

| Data Model | Purpose | Key Attributes |
|------------|---------|----------------|
| `FFit` | Represents a single FITS image, including its data and metadata. | `.data` (NumPy array), `.keywords` (FKeywords object), `.stats` (list of ImageStats), `.header` (str) |
| `Sequence` | Represents an entire image sequence. | `.number` (int), `.seqname` (str), `.imgparam` (list of ImgData), `.regparam` (list of RegData) |
| `PSFStar` | Contains the results of a Point Spread Function (PSF) fit to a star. | `.xpos`, `.ypos`, `.fwhmx`, `.fwhmy`, `.mag`, `.snr`, `.ra`, `.dec` |
| `ImageStats` | Holds detailed statistical information about an image or selection. | `.mean`, `.median`, `.sigma`, `.mad`, `.min`, `.max`, `.bgnoise` |
| `FKeywords` | Provides parsed access to common FITS header keywords. | `.exposure`, `.ccd_temp`, `.gain`, `.focal_length`, `.date_obs` |

## Part 4: Practical Workflows and Code Examples

This section provides complete, executable scripts that demonstrate how to use the `sirilpy` API to perform common, real-world astronomical image processing workflows. Each example is designed to be a practical template that users can adapt for their own data.

### 4.1 Foundational Operations: Loading, Inspecting, and Saving

This script demonstrates the most basic workflow: opening an image, extracting key information from it, and saving it in a different format. This forms the basis for any more complex processing.

**Goal**: Load a FITS image, print its dimensions and exposure time, calculate basic statistics for the first channel, and save the image as a 16-bit TIFF file.

```python
# English: Basic Image Inspection and Saving
import sirilpy as s
import os

# --- Boilerplate Connection ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   print("Failed to connect to Siril. Is it running?")
   quit()

# --- Main Script Logic ---
# Define the input file path. Replace with your file.
# For Windows, use raw strings: r"C:\path\to\image.fit"
input_file = "/path/to/your/image.fit"

if not os.path.exists(input_file):
   siril.error_messagebox(f"Input file not found: {input_file}")
   quit()

try:
   # Load the image into Siril
   siril.cmd("load", input_file)
   siril.log(f"Loaded image: {input_file}")

   # Get the image object (without pixel data for efficiency)
   img = siril.get_image(with_pixels=False)

   # Print image dimensions
   siril.log(f"Image dimensions (HxW): {img.height}x{img.width} pixels, {img.channels} channels.")

   # Get and print exposure time from FITS keywords
   exposure = img.keywords.exposure
   siril.log(f"Exposure time: {exposure} seconds.")

   # Get and print statistics for the first channel (mono/red)
   stats = img.stats
   siril.log(f"Channel 0 Stats: Mean={stats.mean:.4f}, Median={stats.median:.4f}, StdDev={stats.sigma:.4f}")

   # Define output path and save as 16-bit TIFF
   output_file = os.path.splitext(input_file) + ".tif"
   siril.cmd("save", output_file, "-16bit")
   siril.log(f"Image saved as 16-bit TIFF: {output_file}")

except s.CommandError as e:
   siril.error_messagebox(f"A Siril command failed: {e}")
except s.NoImageError:
   siril.error_messagebox("Operation failed because no image was loaded.")
except Exception as e:
   siril.error_messagebox(f"An unexpected error occurred: {e}")
```

```python
# Chinese (简体中文): 基本图像检查与保存
import sirilpy as s
import os

# --- 连接模板 ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   print("连接 Siril 失败。它是否正在运行？")
   quit()

# --- 主脚本逻辑 ---
# 定义输入文件路径。请替换为您的文件路径。
# 对于 Windows，请使用原始字符串: r"C:\path\to\image.fit"
input_file = "/path/to/your/image.fit"

if not os.path.exists(input_file):
   siril.error_messagebox(f"输入文件未找到: {input_file}")
   quit()

try:
   # 将图像加载到 Siril
   siril.cmd("load", input_file)
   siril.log(f"已加载图像: {input_file}")

   # 获取图像对象 (为提高效率，不包含像素数据)
   img = siril.get_image(with_pixels=False)

   # 打印图像尺寸
   siril.log(f"图像尺寸 (高x宽): {img.height}x{img.width} 像素, {img.channels} 通道。")

   # 从 FITS 关键字中获取并打印曝光时间
   exposure = img.keywords.exposure
   siril.log(f"曝光时间: {exposure} 秒。")

   # 获取并打印第一个通道 (单色/红色) 的统计信息
   stats = img.stats
   siril.log(f"通道 0 统计: 平均值={stats.mean:.4f}, 中位值={stats.median:.4f}, 标准差={stats.sigma:.4f}")

   # 定义输出路径并保存为 16 位 TIFF
   output_file = os.path.splitext(input_file) + ".tif"
   siril.cmd("save", output_file, "-16bit")
   siril.log(f"图像已另存为 16 位 TIFF: {output_file}")

except s.CommandError as e:
   siril.error_messagebox(f"Siril 命令执行失败: {e}")
except s.NoImageError:
   siril.error_messagebox("操作失败，因为没有加载图像。")
except Exception as e:
   siril.error_messagebox(f"发生意外错误: {e}")
```

### 4.2 The Complete Pre-processing Workflow (OSC & Monochrome)

This example is the cornerstone of practical automation in Siril. It replicates the functionality of the built-in `OSC_Preprocessing.ssf` script but with the added clarity and modularity of Python. The script assumes the standard Siril directory structure where raw frames are sorted into lights, darks, flats, and biases subdirectories.

**Goal**: Automate the entire pre-processing pipeline: create master calibration frames (bias, dark, flat), then calibrate, register, and stack the light frames to produce a final, high signal-to-noise ratio image.

```python
# English: Full Pre-processing Workflow
import sirilpy as s
import os

# --- Boilerplate Connection ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   quit()

# --- Configuration ---
# Set the main working directory containing lights, darks, etc.
# On Windows: r"C:\Users\YourUser\Astro\M31"
WORK_DIR = "/path/to/your/session/folder"
# Set to True for One-Shot Color (OSC) cameras, False for Monochrome
IS_OSC = True

# --- Helper Functions ---
def check_and_cd(target_dir):
   """Checks if a directory exists and changes Siril's CWD."""
   if not os.path.isdir(target_dir):
       siril.log(f"Directory not found, skipping: {os.path.basename(target_dir)}")
       return False
   siril.cmd("cd", target_dir)
   return True

# --- Main Script Logic ---
try:
   siril.log("Starting full pre-processing workflow...")
   siril.cmd("cd", WORK_DIR)

   # Create a 'process' directory for intermediate files
   process_dir = os.path.join(WORK_DIR, "process")
   if not os.path.exists(process_dir):
       os.makedirs(process_dir)

   # 1. Create Master Bias
   if check_and_cd(os.path.join(WORK_DIR, "biases")):
       siril.log("Processing BIAS frames...")
       siril.cmd("convert", "bias", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)
       siril.cmd("stack", "bias", "rej", "3", "3", "-nonorm")
       siril.log("Master Bias created.")

   # 2. Create Master Dark
   if check_and_cd(os.path.join(WORK_DIR, "darks")):
       siril.log("Processing DARK frames...")
       siril.cmd("convert", "dark", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)
       siril.cmd("stack", "dark", "rej", "3", "3", "-nonorm")
       siril.log("Master Dark created.")

   # 3. Create Master Flat
   if check_and_cd(os.path.join(WORK_DIR, "flats")):
       siril.log("Processing FLAT frames...")
       siril.cmd("convert", "flat", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)
       siril.cmd("preprocess", "flat", "-bias=bias_stacked")
       siril.cmd("stack", "pp_flat", "rej", "3", "3", "-norm=mul")
       siril.log("Master Flat created.")

   # 4. Calibrate, Register, and Stack Lights
   if check_and_cd(os.path.join(WORK_DIR, "lights")):
       siril.log("Processing LIGHT frames...")
       siril.cmd("convert", "light", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)

       # Pre-process lights
       preprocess_cmd = ["preprocess", "light", "-dark=dark_stacked", "-flat=pp_flat_stacked", "-cfa", "-debayer"]
       if not IS_OSC:
           preprocess_cmd.remove("-cfa")
           preprocess_cmd.remove("-debayer")
       siril.cmd(*preprocess_cmd)
       siril.log("Light frame calibration complete.")

       # Register (align) lights
       siril.cmd("register", "pp_light")
       siril.log("Registration complete.")

       # Stack lights
       siril.cmd("stack", "r_pp_light", "rej", "3", "3", "-norm=addscale", "-output_norm", f"-out={os.path.join(WORK_DIR, 'result')}")
       siril.log("Stacking complete.")
       siril.cmd("close")
       siril.info_messagebox(f"Workflow finished! Final image saved as result.fit in {WORK_DIR}")

except s.CommandError as e:
   siril.error_messagebox(f"A Siril command failed: {e}")
except Exception as e:
   siril.error_messagebox(f"An unexpected error occurred: {e}")
```

```python
# Chinese (简体中文): 完整预处理工作流
import sirilpy as s
import os

# --- 连接模板 ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   quit()

# --- 配置 ---
# 设置包含 lights, darks 等的主工作目录
# Windows 示例: r"C:\Users\YourUser\Astro\M31"
WORK_DIR = "/path/to/your/session/folder"
# 彩色相机 (OSC) 设置为 True，单色相机设置为 False
IS_OSC = True

# --- 辅助函数 ---
def check_and_cd(target_dir):
   """检查目录是否存在并更改 Siril 的当前工作目录。"""
   if not os.path.isdir(target_dir):
       siril.log(f"目录未找到，跳过: {os.path.basename(target_dir)}")
       return False
   siril.cmd("cd", target_dir)
   return True

# --- 主脚本逻辑 ---
try:
   siril.log("开始完整预处理工作流...")
   siril.cmd("cd", WORK_DIR)

   # 创建一个 'process' 目录用于存放中间文件
   process_dir = os.path.join(WORK_DIR, "process")
   if not os.path.exists(process_dir):
       os.makedirs(process_dir)

   # 1. 创建主偏置帧 (Master Bias)
   if check_and_cd(os.path.join(WORK_DIR, "biases")):
       siril.log("正在处理 BIAS 帧...")
       siril.cmd("convert", "bias", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)
       siril.cmd("stack", "bias", "rej", "3", "3", "-nonorm")
       siril.log("主偏置帧已创建。")

   # 2. 创建主暗场 (Master Dark)
   if check_and_cd(os.path.join(WORK_DIR, "darks")):
       siril.log("正在处理 DARK 帧...")
       siril.cmd("convert", "dark", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)
       siril.cmd("stack", "dark", "rej", "3", "3", "-nonorm")
       siril.log("主暗场已创建。")

   # 3. 创建主平场 (Master Flat)
   if check_and_cd(os.path.join(WORK_DIR, "flats")):
       siril.log("正在处理 FLAT 帧...")
       siril.cmd("convert", "flat", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)
       siril.cmd("preprocess", "flat", "-bias=bias_stacked")
       siril.cmd("stack", "pp_flat", "rej", "3", "3", "-norm=mul")
       siril.log("主平场已创建。")

   # 4. 校准、对齐和叠加亮场
   if check_and_cd(os.path.join(WORK_DIR, "lights")):
       siril.log("正在处理 LIGHT 帧...")
       siril.cmd("convert", "light", f"-out={process_dir}", "-fitseq")
       siril.cmd("cd", process_dir)

       # 预处理亮场
       preprocess_cmd = ["preprocess", "light", "-dark=dark_stacked", "-flat=pp_flat_stacked", "-cfa", "-debayer"]
       if not IS_OSC:
           preprocess_cmd.remove("-cfa")
           preprocess_cmd.remove("-debayer")
       siril.cmd(*preprocess_cmd)
       siril.log("亮场校准完成。")

       # 对齐亮场
       siril.cmd("register", "pp_light")
       siril.log("对齐完成。")

       # 叠加亮场
       siril.cmd("stack", "r_pp_light", "rej", "3", "3", "-norm=addscale", "-output_norm", f"-out={os.path.join(WORK_DIR, 'result')}")
       siril.log("叠加完成。")
       siril.cmd("close")
       siril.info_messagebox(f"工作流结束！最终图像已保存为 result.fit 在 {WORK_DIR}")

except s.CommandError as e:
   siril.error_messagebox(f"Siril 命令执行失败: {e}")
except Exception as e:
   siril.error_messagebox(f"发生意外错误: {e}")
```

### 4.3 Advanced Astrometry and WCS Manipulation

Astrometry, or plate-solving, is the process of identifying the precise celestial coordinates (Right Ascension and Declination) for every pixel in an image. This is a foundational step for many advanced techniques, including photometric color calibration and object identification. This script demonstrates how to automate plate-solving and use the resulting World Coordinate System (WCS) data.

**Goal**: Load an image, perform a plate-solve using Siril's internal solver, and then use the WCS to find the celestial coordinates of the image center.

```python
# English: Astrometry and WCS Usage
import sirilpy as s
import os

# --- Boilerplate Connection ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   quit()

# --- Configuration ---
IMAGE_FILE = "/path/to/your/unsolved_image.fit"
# These should be known from your equipment
FOCAL_LENGTH_MM = 480.0
PIXEL_SIZE_UM = 3.76

# --- Main Script Logic ---
try:
   siril.cmd("load", IMAGE_FILE)

   # Perform plate-solving
   siril.log("Attempting to plate-solve the image...")
   # The command uses values from FITS header if available,
   # but we can override them for reliability.
   siril.cmd("platesolve", f"-focal={FOCAL_LENGTH_MM}", f"-pixelsize={PIXEL_SIZE_UM}")
   siril.log("Plate-solving successful!")

   # Get the image to access its dimensions
   img = siril.get_image(with_pixels=False)
   center_x = img.width / 2
   center_y = img.height / 2

   # Convert the center pixel coordinates to RA/Dec
   ra_dec = siril.pix2radec(center_x, center_y)
   ra, dec = ra_dec

   # Use astropy for nice formatting of coordinates (optional)
   try:
       s.ensure_installed("astropy")
       from astropy.coordinates import SkyCoord
       import astropy.units as u
       coords = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
       ra_str = coords.ra.to_string(unit=u.hour, sep=':')
       dec_str = coords.dec.to_string(unit=u.degree, sep=':')
       siril.log(f"Image center coordinates: RA={ra_str}, Dec={dec_str}")
   except ImportError:
       siril.log(f"Image center coordinates (decimal degrees): RA={ra:.6f}, Dec={dec:.6f}")

   # Annotate the image with WCS grid
   siril.cmd("setgrid")

except s.CommandError as e:
   siril.error_messagebox(f"Plate-solving failed. Check focal length and pixel size. Error: {e}")
except Exception as e:
   siril.error_messagebox(f"An unexpected error occurred: {e}")
```

```python
# Chinese (简体中文): 天体测量和 WCS 使用
import sirilpy as s
import os

# --- 连接模板 ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   quit()

# --- 配置 ---
IMAGE_FILE = "/path/to/your/unsolved_image.fit"
# 这些信息应从您的设备中获知
FOCAL_LENGTH_MM = 480.0
PIXEL_SIZE_UM = 3.76

# --- 主脚本逻辑 ---
try:
   siril.cmd("load", IMAGE_FILE)

   # 执行天体测量 (板块解析)
   siril.log("正在尝试对图像进行天体测量...")
   # 如果 FITS 头文件中存在，该命令会使用其中的值，
   # 但为确保可靠性，我们可以覆盖它们。
   siril.cmd("platesolve", f"-focal={FOCAL_LENGTH_MM}", f"-pixelsize={PIXEL_SIZE_UM}")
   siril.log("天体测量成功！")

   # 获取图像以访问其尺寸
   img = siril.get_image(with_pixels=False)
   center_x = img.width / 2
   center_y = img.height / 2

   # 将中心像素坐标转换为赤经/赤纬
   ra_dec = siril.pix2radec(center_x, center_y)
   ra, dec = ra_dec

   # 使用 astropy 进行坐标的优美格式化 (可选)
   try:
       s.ensure_installed("astropy")
       from astropy.coordinates import SkyCoord
       import astropy.units as u
       coords = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
       ra_str = coords.ra.to_string(unit=u.hour, sep=':')
       dec_str = coords.dec.to_string(unit=u.degree, sep=':')
       siril.log(f"图像中心坐标: RA={ra_str}, Dec={dec_str}")
   except ImportError:
       siril.log(f"图像中心坐标 (十进制度): RA={ra:.6f}, Dec={dec:.6f}")

   # 使用 WCS 网格注释图像
   siril.cmd("setgrid")

except s.CommandError as e:
   siril.error_messagebox(f"天体测量失败。请检查焦距和像素大小。错误: {e}")
except Exception as e:
   siril.error_messagebox(f"发生意外错误: {e}")
```

### 4.4 Scientific Photometry: Generating a Light Curve

Photometry is the measurement of the brightness of astronomical objects. By performing photometry on a sequence of images, one can create a light curve, which plots an object's brightness over time. This is a fundamental technique for studying variable stars and detecting exoplanet transits.

**Goal**: Load a registered sequence of a variable star, allow the user to select the variable star and a stable comparison star, then perform aperture photometry on both stars in every frame. Finally, calculate the differential magnitude and plot the resulting light curve using Siril's native plotting tool.

```python
# English: Light Curve Photometry
import sirilpy as s

# --- Boilerplate Connection ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   quit()

# --- Main Script Logic ---
try:
   if not siril.is_sequence_loaded():
       siril.error_messagebox("Please load a registered sequence first.")
       quit()

   # 1. Get user to select the variable star
   siril.info_messagebox("Please draw a selection around the VARIABLE star and click OK.")
   variable_star_selection = siril.get_siril_selection()
   if not variable_star_selection:
       siril.error_messagebox("No selection made. Aborting.")
       quit()

   # 2. Get user to select the comparison star
   siril.info_messagebox("Please draw a selection around a non-variable COMPARISON star of similar brightness and click OK.")
   comparison_star_selection = siril.get_siril_selection()
   if not comparison_star_selection:
       siril.error_messagebox("No selection made. Aborting.")
       quit()

   # 3. Iterate through the sequence and perform photometry
   seq = siril.get_seq()
   num_frames = seq.number
   timestamps = []
   diff_mags = []

   siril.log("Starting photometry on sequence...")
   for i in range(num_frames):
       siril.update_progress(f"Processing frame {i+1}/{num_frames}", (i+1)/num_frames)

       # Load the current frame
       siril.cmd("goseq", str(i))

       # Photometry on variable star
       siril.set_siril_selection(selection=variable_star_selection)
       siril.cmd("psf")
       var_star = siril.get_image_stars() # Assume first star found in selection is the target

       # Photometry on comparison star
       siril.set_siril_selection(selection=comparison_star_selection)
       siril.cmd("psf")
       comp_star = siril.get_image_stars()

       # Calculate differential magnitude and store data
       if var_star and comp_star:
           diff_mag = var_star.mag - comp_star.mag
           diff_mags.append(diff_mag)
           
           frame_info = siril.get_seq_imgdata(i)
           timestamps.append(frame_info.date_obs.timestamp())

   siril.reset_progress()
   siril.log("Photometry complete.")

   # 4. Plot the light curve
   if timestamps and diff_mags:
       # Normalize timestamps to start from 0 hours
       start_time = min(timestamps)
       time_hours = [(t - start_time) / 3600.0 for t in timestamps]

       plot = s.PlotData(
           title="Differential Light Curve",
           xlabel="Time (hours)",
           ylabel="Differential Magnitude"
       )
       plot.add_series(time_hours, diff_mags, label="Variable Star", plot_type=s.PlotType.POINTS)
       siril.xy_plot(plot)
   else:
       siril.warning_messagebox("No valid photometric data was collected.")

except Exception as e:
   siril.reset_progress()
   siril.error_messagebox(f"An error occurred: {e}")
```

```python
# Chinese (简体中文): 光变曲线测光
import sirilpy as s

# --- 连接模板 ---
siril = s.SirilInterface()
try:
   siril.connect()
except s.SirilConnectionError:
   quit()

# --- 主脚本逻辑 ---
try:
   if not siril.is_sequence_loaded():
       siril.error_messagebox("请先加载一个已对齐的序列。")
       quit()

   # 1. 让用户选择变星
   siril.info_messagebox("请在变星周围绘制一个选区，然后点击"确定"。")
   variable_star_selection = siril.get_siril_selection()
   if not variable_star_selection:
       siril.error_messagebox("未制作选区。正在中止。")
       quit()

   # 2. 让用户选择比较星
   siril.info_messagebox("请在亮度相近的非变星（比较星）周围绘制一个选区，然后点击"确定"。")
   comparison_star_selection = siril.get_siril_selection()
   if not comparison_star_selection:
       siril.error_messagebox("未制作选区。正在中止。")
       quit()

   # 3. 遍历序列并执行测光
   seq = siril.get_seq()
   num_frames = seq.number
   timestamps = []
   diff_mags = []

   siril.log("开始对序列进行测光...")
   for i in range(num_frames):
       siril.update_progress(f"正在处理帧 {i+1}/{num_frames}", (i+1)/num_frames)

       # 加载当前帧
       siril.cmd("goseq", str(i))

       # 对变星进行测光
       siril.set_siril_selection(selection=variable_star_selection)
       siril.cmd("psf")
       var_star = siril.get_image_stars() # 假设选区中找到的第一颗星是目标

       # 对比较星进行测光
       siril.set_siril_selection(selection=comparison_star_selection)
       siril.cmd("psf")
       comp_star = siril.get_image_stars()

       # 计算较差星等并存储数据
       if var_star and comp_star:
           diff_mag = var_star.mag - comp_star.mag
           diff_mags.append(diff_mag)
           
           frame_info = siril.get_seq_imgdata(i)
           timestamps.append(frame_info.date_obs.timestamp())

   siril.reset_progress()
   siril.log("测光完成。")

   # 4. 绘制光变曲线
   if timestamps and diff_mags:
       # 将时间戳归一化，从 0 小时开始
       start_time = min(timestamps)
       time_hours = [(t - start_time) / 3600.0 for t in timestamps]

       plot = s.PlotData(
           title="较差光变曲线",
           xlabel="时间 (小时)",
           ylabel="较差星等"
       )
       plot.add_series(time_hours, diff_mags, label="变星", plot_type=s.PlotType.POINTS)
       siril.xy_plot(plot)
   else:
       siril.warning_messagebox("未收集到有效的光度数据。")

except Exception as e:
   siril.reset_progress()
   siril.error_messagebox(f"发生错误: {e}")
```

## Part 5: Integration with the Scientific Python Ecosystem

The true power of `sirilpy` is unlocked when it is used not as an isolated tool, but as a high-performance component within the broader scientific Python ecosystem. The bridge between Siril and other libraries is the NumPy array. By retrieving pixel data from Siril into a standard NumPy array, users can leverage the vast array of specialized algorithms available in libraries like Astropy and Photutils. The results can then be passed back into Siril for visualization or further processing. This "round-trip" capability enables the creation of hybrid, best-of-breed workflows that combine the strengths of multiple tools.

### 5.1 Siril and astropy: Advanced FITS Handling

While Siril provides excellent tools for most FITS operations, `astropy.io.fits` offers unparalleled control over the intricacies of the FITS header. This example shows how to use Siril for processing and then leverage astropy for fine-grained header manipulation.

**Goal**: Load an image in Siril, get its header, use astropy to add a new custom keyword, and then update the header metadata back in Siril.

```python
# English: Advanced FITS Header Manipulation with Astropy
import sirilpy as s
s.ensure_installed("astropy")
from astropy.io import fits
import io

# --- Boilerplate Connection ---
siril = s.SirilInterface()
try:
   siril.connect()
   siril.cmd("load", "/path/to/your/image.fit")
except Exception as e:
   print(f"Setup failed: {e}")
   quit()

# --- Main Logic ---
try:
   with siril.image_lock():
       # 1. Get the header string from Siril
       header_str = siril.get_image_fits_header()

       # 2. Use Astropy to parse and modify the header
       # We read the string into an in-memory file to parse it
       with io.StringIO(header_str) as f:
           header_obj = fits.Header.fromfile(f)

       # Add a new keyword
       header_obj['MYSCRIPT'] = ('Observer who ran this script', 'My Script')
       header_obj['SIRILPY'] = (s.utility.check_module_version(), 'SirilPy module version')

       # 3. Convert the modified header back to a string
       modified_header_str = header_obj.tostring(sep='\n', endcard=False, padding=False)

       # 4. Send the updated header back to Siril
       siril.set_image_metadata_from_header_string(modified_header_str)
       siril.log("FITS header updated with custom keywords using Astropy.")

except Exception as e:
   siril.error_messagebox(f"An error occurred: {e}")
```

```python
# Chinese (简体中文): 使用 Astropy 进行高级 FITS 头文件操作
import sirilpy as s
s.ensure_installed("astropy")
from astropy.io import fits
import io

# --- 连接模板 ---
siril = s.SirilInterface()
try:
   siril.connect()
   siril.cmd("load", "/path/to/your/image.fit")
except Exception as e:
   print(f"设置失败: {e}")
   quit()

# --- 主逻辑 ---
try:
   with siril.image_lock():
       # 1. 从 Siril 获取头文件字符串
       header_str = siril.get_image_fits_header()

       # 2. 使用 Astropy 解析和修改头文件
       # 我们将字符串读入内存中的文件进行解析
       with io.StringIO(header_str) as f:
           header_obj = fits.Header.fromfile(f)

       # 添加一个新的关键字
       header_obj['MYSCRIPT'] = ('运行此脚本的观测者', 'My Script')
       header_obj['SIRILPY'] = (s.utility.check_module_version(), 'SirilPy 模块版本')

       # 3. 将修改后的头文件转换回字符串
       modified_header_str = header_obj.tostring(sep='\n', endcard=False, padding=False)

       # 4. 将更新后的头文件发送回 Siril
       siril.set_image_metadata_from_header_string(modified_header_str)
       siril.log("已使用 Astropy 更新 FITS 头文件中的自定义关键字。")

except Exception as e:
   siril.error_messagebox(f"发生错误: {e}")
```

### 5.2 Advanced Source Detection with photutils

Siril's `findstar` command is fast and effective for many tasks, but `photutils` offers a suite of more advanced and configurable source detection algorithms, such as `DAOStarFinder` and `IRAFStarFinder`. This workflow demonstrates how to perform pre-processing in Siril, extract the image data for analysis in `photutils`, and then visualize the results back in the Siril GUI. This pattern combines Siril's high-performance C++ core for I/O-heavy tasks with Python's specialized analysis libraries.

**Goal**: Stack an image in Siril, pass the result to `photutils` to detect stars, and draw circles around the detected stars on the Siril image overlay.

```python
# English: Source Detection with Photutils and Overlay Visualization
import sirilpy as s
import numpy as np

s.ensure_installed("astropy")
s.ensure_installed("photutils")

from astropy.stats import mad_std
from photutils.detection import DAOStarFinder

# --- Boilerplate Connection ---
siril = s.SirilInterface()
try:
   siril.connect()
   # Assume an image is already loaded and processed (e.g., stacked result)
   if not siril.is_image_loaded():
       siril.error_messagebox("Load a stacked image before running.")
       quit()
except Exception as e:
   quit()

# --- Main Logic ---
try:
   siril.log("Performing advanced source detection with Photutils...")
   with siril.image_lock():
       # 1. Get image data from Siril
       image_data = siril.get_image_pixeldata()
       # Photutils works best on 2D mono data
       if image_data.ndim == 3:
           # Convert to grayscale/luminance
           image_data = 0.2126 * image_data[:,:,0] + 0.7152 * image_data[:,:,1] + 0.0722 * image_data[:,:,2]

       # 2. Use Photutils for source detection
       bkg_sigma = mad_std(image_data)
       daofind = DAOStarFinder(fwhm=5.0, threshold=5.*bkg_sigma)
       sources = daofind(image_data)

       if sources is None:
           siril.warning_messagebox("Photutils found no sources.")
           quit()
       
       siril.log(f"Photutils detected {len(sources)} sources.")

       # 3. Visualize results back in Siril using overlays
       siril.overlay_clear_polygons() # Clear previous overlays
       for star in sources:
           x, y = star['xcentroid'], star['ycentroid']
           # Create a circular polygon to mark the star
           radius = 10
           rect = (x - radius, y - radius, 2 * radius, 2 * radius)
           # A circle is just a rectangle with a legend indicating it's a

circle, Siril's overlay will render it as a circle if the legend starts with 'circle'
           poly = s.Polygon.from_rectangle(rect, legend="circle", color=0xFF0000A0) # Red, semi-transparent
           siril.overlay_add_polygon(poly)
       
       siril.info_messagebox("Source detection complete. Results are shown on the image overlay.")

except Exception as e:
   siril.error_messagebox(f"An error occurred during Photutils processing: {e}")
```

```python
# Chinese (简体中文): 使用 Photutils 进行源检测和叠加可视化
import sirilpy as s
import numpy as np

s.ensure_installed("astropy")
s.ensure_installed("photutils")

from astropy.stats import mad_std
from photutils.detection import DAOStarFinder

# --- 连接模板 ---
siril = s.SirilInterface()
try:
   siril.connect()
   # 假设已加载并处理了图像 (例如，叠加结果)
   if not siril.is_image_loaded():
       siril.error_messagebox("运行前请加载一张已叠加的图像。")
       quit()
except Exception as e:
   quit()

# --- 主逻辑 ---
try:
   siril.log("正在使用 Photutils 进行高级源检测...")
   with siril.image_lock():
       # 1. 从 Siril 获取图像数据
       image_data = siril.get_image_pixeldata()
       # Photutils 在 2D 单色数据上效果最佳
       if image_data.ndim == 3:
           # 转换为灰度/亮度
           image_data = 0.2126 * image_data[:,:,0] + 0.7152 * image_data[:,:,1] + 0.0722 * image_data[:,:,2]

       # 2. 使用 Photutils 进行源检测
       bkg_sigma = mad_std(image_data)
       daofind = DAOStarFinder(fwhm=5.0, threshold=5.*bkg_sigma)
       sources = daofind(image_data)

       if sources is None:
           siril.warning_messagebox("Photutils 未找到任何源。")
           quit()
       
       siril.log(f"Photutils 检测到 {len(sources)} 个源。")

       # 3. 使用叠加层在 Siril 中将结果可视化
       siril.overlay_clear_polygons() # 清除之前的叠加层
       for star in sources:
           x, y = star['xcentroid'], star['ycentroid']
           # 创建一个圆形多边形来标记恒星
           radius = 10
           rect = (x - radius, y - radius, 2 * radius, 2 * radius)
           # 圆形只是一个带有图例的矩形，表明它是一个圆
           # 如果图例以 'circle' 开头，Siril 的叠加层会将其渲染为圆形
           poly = s.Polygon.from_rectangle(rect, legend="circle", color=0xFF0000A0) # 红色，半透明
           siril.overlay_add_polygon(poly)
       
       siril.info_messagebox("源检测完成。结果显示在图像叠加层上。")

except Exception as e:
   siril.error_messagebox(f"在 Photutils 处理期间发生错误: {e}")
```

### 5.3 Custom Data Visualization with matplotlib

While Siril's built-in `xy_plot` is convenient for quick data visualization, matplotlib is the industry standard for creating customizable, publication-quality plots in Python. This example extends the photometry workflow by using matplotlib to generate a high-quality light curve plot and save it as a PNG file.

**Goal**: Perform the light curve analysis from section 4.4, but instead of using `xy_plot`, generate a detailed plot with matplotlib and save it to disk.

```python
# English: Publication-Quality Plotting with Matplotlib
import sirilpy as s
import os
s.ensure_installed("matplotlib")
import matplotlib.pyplot as plt

# --- Assume photometry data (time_hours, diff_mags) has been generated
# --- as in the example from section 4.4. For this standalone example,
# --- we will use placeholder data.

# Placeholder data
time_hours = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
diff_mags = [0.01, 0.00, -0.01, 0.02, 0.5, 0.48, 0.01, 0.00]
object_name = "My Variable Star"
output_dir = "/path/to/your/session/folder"

# --- Main Plotting Logic ---
try:
   plt.style.use('seaborn-v0_8-darkgrid')
   fig, ax = plt.subplots(figsize=(10, 6))

   # Scatter plot of the data points
   ax.scatter(time_hours, diff_mags, color='royalblue', label='Observations')
   
   # Invert y-axis for magnitude plot
   ax.invert_yaxis()

   # Set titles and labels
   ax.set_title(f'Differential Light Curve for {object_name}', fontsize=16)
   ax.set_xlabel('Time Since First Observation (hours)', fontsize=12)
   ax.set_ylabel('Differential Magnitude', fontsize=12)
   ax.legend()
   ax.grid(True)

   # Save the plot
   output_path = os.path.join(output_dir, f"{object_name}_light_curve.png")
   plt.savefig(output_path, dpi=300, bbox_inches='tight')
   
   # Use Siril to notify the user
   siril = s.SirilInterface()
   siril.connect()
   siril.info_messagebox(f"Light curve plot saved to: {output_path}")

except Exception as e:
   print(f"An error occurred during plotting: {e}")
```

```python
# Chinese (简体中文): 使用 Matplotlib 进行出版级绘图
import sirilpy as s
import os
s.ensure_installed("matplotlib")
import matplotlib.pyplot as plt

# --- 假设已经生成了测光数据 (time_hours, diff_mags)
# --- 如 4.4 节中的示例。对于这个独立示例，
# --- 我们将使用占位符数据。

# 占位符数据
time_hours = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
diff_mags = [0.01, 0.00, -0.01, 0.02, 0.5, 0.48, 0.01, 0.00]
object_name = "我的变星"
output_dir = "/path/to/your/session/folder"

# --- 主绘图逻辑 ---
try:
   plt.style.use('seaborn-v0_8-darkgrid')
   fig, ax = plt.subplots(figsize=(10, 6))

   # 数据点的散点图
   ax.scatter(time_hours, diff_mags, color='royalblue', label='观测数据')
   
   # 反转 y 轴以绘制星等图
   ax.invert_yaxis()

   # 设置标题和标签
   ax.set_title(f'{object_name} 的较差光变曲线', fontsize=16)
   ax.set_xlabel('自首次观测以来的时间 (小时)', fontsize=12)
   ax.set_ylabel('较差星等', fontsize=12)
   ax.legend()
   ax.grid(True)

   # 保存绘图
   output_path = os.path.join(output_dir, f"{object_name}_light_curve.png")
   plt.savefig(output_path, dpi=300, bbox_inches='tight')
   
   # 使用 Siril 通知用户
   siril = s.SirilInterface()
   siril.connect()
   siril.info_messagebox(f"光变曲线图已保存至: {output_path}")

except Exception as e:
   print(f"绘图期间发生错误: {e}")
```

## Part 6: Best Practices and Advanced Topics

### 6.1 Performance Optimization

While Siril is highly optimized for performance, script design and system configuration can have a significant impact on execution speed, especially when processing large datasets. Following these best practices can dramatically reduce processing times.

* **Prioritize Fast Storage**: Siril is extremely disk I/O heavy. The process of reading hundreds or thousands of large RAW or FITS files is often the primary bottleneck.
  * *Recommendation*: Always store and process image data on the fastest available drive. An NVMe SSD is ideal, followed by a SATA SSD. Processing on a traditional spinning hard disk drive (HDD) will be significantly slower.
* **Use FITS Sequences (`-fitseq`)**: When converting raw files (e.g., from a DSLR or astronomy camera), use the `-fitseq` argument with the `convert` command. This creates a single large FITS file (a "FITS cube") containing all the images in the sequence, rather than hundreds of individual `.fit` files. When Siril processes this sequence, it can read the entire file into memory at once or access frames more efficiently, drastically reducing disk I/O operations and improving overall speed.
  * *Example*: `siril.cmd("convert", "light", "-fitseq")`
* **Allocate Sufficient Memory**: In Siril's preferences (under "Performance"), ensure that the memory allocation is set to a reasonable fraction of your system's total RAM. If Siril is memory-constrained, it will have to page data to and from the disk more frequently, slowing down operations.
* **Understand Algorithmic Trade-offs**: Different processing choices have different performance characteristics. For example, using Bayer Drizzle during registration can sometimes be faster than performing a separate high-quality debayering step followed by registration, as it combines two operations. However, drizzle itself is computationally intensive. It is worthwhile to experiment with different workflows on a subset of data to find the most efficient method for a specific hardware setup and dataset.
* **Process Fewer, Longer Exposures**: The total processing time is more dependent on the number of frames than the total integration time. Processing 100 frames of 5-minute exposures will be much faster than processing 500 frames of 1-minute exposures, even though the total exposure time is the same.

### 6.2 Robust Error Handling and Debugging

Writing robust scripts involves anticipating and gracefully handling potential errors. The `sirilpy` API provides specific exceptions that allow for more targeted error handling than a generic `try...except Exception`.

* **Catch Specific Exceptions**: Instead of a single broad `except` block, catch specific exceptions like `s.CommandError`, `s.NoImageError`, or `s.ProcessingThreadBusyError`. This allows the script to provide more precise feedback to the user about what went wrong.
* **Use State-Checking Functions**: Before attempting an operation, use functions like `siril.is_image_loaded()` or `siril.is_sequence_loaded()` to verify that the application is in the correct state. This is a form of "defensive programming" that can prevent errors before they occur.
* **Provide User Feedback**: When an error is caught, use `siril.error_messagebox()` to display a clear, user-friendly message explaining the problem and suggesting a solution. For non-critical issues, use `siril.warning_messagebox()`.
* **Debug Commands Interactively**: If a `cmd()` call is failing with a `CommandError`, the fastest way to debug it is to copy the command and its arguments and run them directly in the Siril command line at the bottom of the main window. The console will often provide more detailed error messages than are available to the script.

```python
# English: Robust Error Handling Example
def process_image(file_path):
   if not siril.is_image_loaded():
       siril.warning_messagebox("No image loaded. Loading now.")
       try:
           siril.cmd("load", file_path)
       except s.CommandError:
           siril.error_messagebox(f"Failed to load image: {file_path}")
           return False

   try:
       siril.cmd("autostretch")
       # This command will fail if the image is not color
       siril.cmd("pcc")
       return True
   except s.CommandError as e:
       # Check the error message to provide a specific suggestion
       if "Image must be a color image" in str(e):
           siril.error_messagebox("Photometric Color Calibration requires a color image. This image appears to be monochrome.")
       else:
           siril.error_messagebox(f"An error occurred during processing: {e}")
       return False
```

```python
# Chinese (简体中文): 稳健的错误处理示例
def process_image(file_path):
   if not siril.is_image_loaded():
       siril.warning_messagebox("没有加载图像。现在加载。")
       try:
           siril.cmd("load", file_path)
       except s.CommandError:
           siril.error_messagebox(f"加载图像失败: {file_path}")
           return False

   try:
       siril.cmd("autostretch")
       # 如果图像不是彩色的，此命令将失败
       siril.cmd("pcc")
       return True
   except s.CommandError as e:
       # 检查错误消息以提供具体建议
       if "Image must be a color image" in str(e):
           siril.error_messagebox("光度颜色校准需要彩色图像。此图像似乎是单色的。")
       else:
           siril.error_messagebox(f"处理过程中发生错误: {e}")
       return False
```

### 6.3 Batch Processing and Script Organization

For processing multiple nights of data or different targets, scripts should be designed to run in batches. This involves using Python's standard libraries for file system navigation to iterate over a set of directories.

* **Isolate Logic in Functions**: Encapsulate the core processing workflow into a function that accepts a directory path as an argument.
* **Use os and glob**: Use the `os` module to work with paths and the `glob` module to find all directories matching a certain pattern.
* **Loop and Process**: Create a main loop that iterates through the discovered directories and calls the processing function for each one.

```python
# English: Batch Processing Multiple Directories
import os
import glob

# Assume the full_preprocessing_workflow function from section 4.2 is defined here
def full_preprocessing_workflow(work_dir, is_osc):
   #... (processing logic from section 4.2)...
   siril.log(f"Finished processing {work_dir}")

# --- Main Batch Logic ---
# Parent directory containing multiple session folders (e.g., Night1, Night2)
parent_dir = "/path/to/all/sessions"
session_folders = glob.glob(os.path.join(parent_dir, "Night*"))

for folder in session_folders:
   if os.path.isdir(folder):
       siril.log(f"--- Starting processing for: {folder} ---")
       full_preprocessing_workflow(folder, is_osc=True)

siril.info_messagebox("Batch processing complete for all sessions.")
```

```python
# Chinese (简体中文): 批量处理多个目录
import os
import glob

# 假设此处定义了 4.2 节中的 full_preprocessing_workflow 函数
def full_preprocessing_workflow(work_dir, is_osc):
   #... (来自 4.2 节的处理逻辑)...
   siril.log(f"完成处理 {work_dir}")

# --- 主批量处理逻辑 ---
# 包含多个会话文件夹 (例如 Night1, Night2) 的父目录
parent_dir = "/path/to/all/sessions"
session_folders = glob.glob(os.path.join(parent_dir, "Night*"))

for folder in session_folders:
   if os.path.isdir(folder):
       siril.log(f"--- 开始处理: {folder} ---")
       full_preprocessing_workflow(folder, is_osc=True)

siril.info_messagebox("所有会话的批量处理已完成。")
```

## Part 7: Troubleshooting and FAQ

This section addresses common issues encountered when writing and running `sirilpy` scripts, along with their solutions.

* **Issue**: Script fails immediately with `SirilConnectionError: Connection failed`.
  * **Cause**: The script cannot communicate with the Siril application.
  * **Solution**:
    1. Ensure that Siril is running before you execute the script. `sirilpy` scripts are run from within Siril's script menu and connect to the instance they were launched from.
    2. Verify that you are not attempting to run a `sirilpy` script as a standalone Python file. For standalone automation, the `pysiril` library should be used instead.

* **Issue**: A command fails with `NoImageError` or `NoSequenceError`.
  * **Cause**: The script is attempting to perform an operation that requires an image or sequence to be loaded, but one is not.
  * **Solution**:
    1. Before any processing commands, ensure your script explicitly loads an image (`siril.cmd("load", "image.fit")`) or sets a working directory and allows a sequence to be detected (`siril.cmd("cd", "/path/to/lights")`).
    2. Use defensive checks like `if siril.is_image_loaded():` before calling functions that depend on an image being present.

* **Issue**: An import statement fails with `ModuleNotFoundError: No module named 'astropy'`.
  * **Cause**: The required third-party library is not installed in Siril's managed venv.
  * **Solution**: Add the line `s.ensure_installed("astropy")` (or the name of the missing module) before the `import astropy` line in your script. This will trigger the automatic installation of the module.

* **Issue**: Siril becomes unresponsive or crashes when the script modifies image data.
  * **Cause**: This is a classic symptom of a race condition, where the script and another part of Siril are trying to access the same image memory buffer simultaneously.
  * **Solution**: Ensure that any block of code that reads pixel data (`get_image_pixeldata`), modifies it, and writes it back (`set_image_pixeldata`) is wrapped in a `with siril.image_lock():` statement. This guarantees exclusive access and prevents crashes.

* **Issue**: A `cmd()` call fails with a generic `CommandError`, and the reason is not obvious.
  * **Cause**: The command was passed invalid arguments, or the state of the application was not suitable for that command.
  * **Solution**:
    1. Add a `print()` or `siril.log()` statement just before the failing `cmd()` call to display the exact command and all its arguments as the script sees them.
    2. Manually type or paste this exact command and its arguments into the Siril command line at the bottom of the GUI. The Siril console will usually provide a more verbose and informative error message that can help diagnose the problem.

## Appendix: English-Chinese Glossary of Terms

This glossary provides standardized translations for key technical terms used throughout this documentation and within the Siril software. The Chinese terms are consistent with those used in the official Siril Chinese documentation to ensure clarity and avoid ambiguity.

| English Term | Chinese Term (简体中文) | Description |
|--------------|------------------------|-------------|
| Astrometry | 天体测量 | The science of measuring the positions and movements of celestial objects. |
| Aperture Photometry | 孔径测光 | Measuring the flux of an object by summing the pixel values within a circular aperture. |
| Background Extraction | 背景提取 | The process of removing gradients and uneven illumination from an image. |
| Bias Frame | 偏置帧 | A zero-exposure image capturing the readout noise of the camera sensor. |
| Calibration | 校准 | The process of removing instrumental signatures using bias, dark, and flat frames. |
| Color Calibration | 颜色校准 | Adjusting the color balance of an image to reflect the true colors of celestial objects. |
| Command | 命令 | A text-based instruction given to Siril to perform an action. |
| Dark Frame | 暗场 | A long-exposure image taken with the lens cap on to capture thermal noise. |
| Debayering | 德拜耳 (去马赛克) | The process of reconstructing a full-color image from the raw data of a color sensor. |
| Deconvolution | 反卷积 | An image processing technique to reduce blurring and enhance detail. |
| Drizzle | Drizzle (细雨算法) | A registration and stacking technique that can improve resolution and reduce artifacts. |
| FITS (Flexible Image Transport System) | FITS (灵活图像传输系统) | The standard data format for storing, transmitting, and processing astronomical images. |
| Flat Frame | 平场 | An image of an evenly illuminated surface used to correct for vignetting and dust motes. |
| FWHM (Full Width at Half Maximum) | 半峰全宽 (FWHM) | A measure of the width of a star's profile, often used to quantify seeing or focus quality. |
| Histogram | 直方图 | A graphical representation of the tonal distribution in an image. |
| Light Frame | 亮场 | The primary images of the astronomical target. |
| Photometry | 测光 | The measurement of the brightness or flux of astronomical objects. |
| Plate Solving | 板块解析 | The process of calculating the astrometric solution (WCS) for an image. |
| Pre-processing | 预处理 | The initial calibration stage of the workflow (bias, dark, flat correction). |
| PSF (Point Spread Function) | 点扩散函数 (PSF) | The response of an imaging system to a point source (i.e., how it smears out a star). |
| Registration | 对齐 (配准) | The process of aligning a sequence of images to a common reference frame. |
| Sequence | 序列 | A series of images treated as a single group in Siril. |
| Signal-to-Noise Ratio (SNR) | 信噪比 (SNR) | A measure of the quality of a signal, comparing the level of the desired signal to the level of background noise. |
| Stacking | 叠加 | The process of combining multiple registered images to improve the signal-to-noise ratio. |
| Virtual Environment (venv) | 虚拟环境 (venv) | An isolated Python environment that Siril uses to manage script dependencies. |
| WCS (World Coordinate System) | 世界坐标系 (WCS) | A system that maps the pixels in an image to real-world celestial coordinates. |

## Works cited

1. Siril 1.4.0 Beta 1, accessed on August 16, 2025, <https://siril.org/download/2025-04-26-siril-1-4-0-beta1/>
2. Automating with pySiril - Siril, accessed on August 16, 2025, <https://siril.org/tutorials/pysiril/>
3. Python Scripts — Siril 1.4.0-beta3 documentation, accessed on August 16, 2025, <https://siril.readthedocs.io/en/stable/scripts/Python-scripts.html>
4. Siril python scripting - Astronomy Software & Computers - Cloudy Nights, accessed on August 16, 2025, <https://www.cloudynights.com/topic/952707-siril-python-scripting/>
5. FAQ - Siril, accessed on August 16, 2025, <https://siril.org/faq/>
6. Siril's New Python Integration! Full Tour of the Scripts Environment - YouTube, accessed on August 16, 2025, <https://www.youtube.com/watch?v=qgOW9mSE8wk>
7. Siril 1.4.0 Beta 3, accessed on August 16, 2025, <https://siril.org/download/2025-07-11-siril-1-4-0-beta3/>
8. FA / Siril - GitLab, accessed on August 16, 2025, <https://gitlab.com/free-astro/siril>
9. Python Script Key Information - Siril's documentation! - Read the Docs, accessed on August 16, 2025, <https://siril.readthedocs.io/en/latest/scripts/pykeyinfo.html>
10. Sirilpy Python Module API 0.7.55 Reference — Siril 1.4.0-beta3 ..., accessed on August 16, 2025, <https://siril.readthedocs.io/en/latest/Python-API.html>
11. Full image processing (pre-processed with scripts) - Siril, accessed on August 16, 2025, <https://siril.org/tutorials/tuto-scripts/>
12. Plate Solving in Siril Explained - YouTube, accessed on August 16, 2025, <https://www.youtube.com/watch?v=iF_NaOIOH58>
13. Photometry - Siril, accessed on August 16, 2025, <https://siril.org/tutorials/photometry/>
14. L05: Relative Photometry | PHY241 - GitHub Pages, accessed on August 16, 2025, <https://sheffield-mps.github.io/PHY241/lectures/l05/>
15. Photutils — photutils 2.2.0, accessed on August 16, 2025, <https://photutils.readthedocs.io/>
16. PSF Photometry (photutils.psf) - Read the Docs, accessed on August 16, 2025, <https://photutils.readthedocs.io/en/stable/user_guide/psf.html>
17. Is there a way to make Siril run faster? : r/AskAstrophotography - Reddit, accessed on August 16, 2025, <https://www.reddit.com/r/AskAstrophotography/comments/1gbg3nk/is_there_a_way_to_make_siril_run_faster/>
18. Siril Preprocessing Script for Seestars (both regular and mosaic modes) - Smart Telescopes, accessed on August 16, 2025, <https://www.cloudynights.com/topic/964610-siril-preprocessing-script-for-seestars-both-regular-and-mosaic-modes/>
19. 欢迎来到Siril的文档！ — Siril 1.4.0-beta3 文档 - Read the Docs, accessed on August 16, 2025, <https://siril.readthedocs.io/zh_CN/stable/>
