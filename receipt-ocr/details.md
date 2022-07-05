# Source
 > https://pypi.org/project/pytesseract/


# Functions

### get_languages
Returns all currently supported languages by Tesseract OCR

### get_tesseract_version
Returns the Tesseract version installed in the system

### image_to_string
Returns unmodified output as string from Tesseract OCR processing

### image_to_boxes
Returns result containing recognized characters and their box boundaries

### image_to_data
Returns result containing box boundaries, confidences, and other information. Requires Tesseract 3.05+. For more information, please check the Tesseract TSV documentation

### image_to_osd
Returns result containing information about orientation and script detection

### image_to_alto_xml
Returns result in the form of Tesseract’s ALTO XML format

### run_and_get_output
Returns the raw output from Tesseract OCR. Gives a bit more control over the parameters that are sent to tesseract


# Parameters
 > image_to_data(image, lang=None, config='', nice=0, output_type=Output.STRING, timeout=0, pandas_config=None)

### image `Object` or `String`
PIL Image/NumPy array or file path of the image to be processed by Tesseract.
If you pass object instead of file path, pytesseract will implicitly convert the image to RGB mode

### lang `String`
Tesseract language code string. Defaults to eng if not specified! Example for multiple languages: lang='eng+fra'

### config `String`
Any additional custom configuration flags that are not available via the pytesseract function
For example: config='--psm 6'

### nice `Integer`
Modifies the processor priority for the Tesseract run. Not supported on Windows.
Nice adjusts the niceness of unix-like processes

### output_type `Class attribute`
Specifies the type of the output, defaults to string. For the full list of all supported types,
please check the definition of pytesseract.Output class

### timeout `Integer` or `Float`
Duration in seconds for the OCR processing, after which, pytesseract will terminate and raise RuntimeError

### pandas_config `Dict`
Only for the Output.DATAFRAME type. Dictionary with custom arguments for pandas.read_csv.
Allows you to customize the output of `image_to_data`
