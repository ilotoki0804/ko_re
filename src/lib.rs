use pyo3::{exceptions::{PyTypeError, PyValueError}, prelude::*};
use korean_regex::{Order, KoreanRegexError};

#[pyfunction]
fn compilestr(pattern: &str, order: Option<&str>) -> PyResult<String> {
    let order: Order = match order {
        Some("default") | None => Order::Default,
        Some("regular_first") => Order::RegularFirst,
        _ => return Err(PyTypeError::new_err("`Order` must be `None`, `default` or `regular_first`.")),
    };

    match korean_regex::compilestr(pattern, order) {
        Ok(result) => Ok(result),
        Err(reason) => {
            match reason {
                KoreanRegexError::UnparenthesizingFailedError(msg)
                | KoreanRegexError::InvalidHyphenError(msg)
                | KoreanRegexError::InvalidZeroPatternError(msg)
                => Err(PyValueError::new_err(msg)),
                KoreanRegexError::InvalidPhonemeError(msg, _)
                => Err(PyValueError::new_err(msg)),
                KoreanRegexError::RegexError(regex_err)
                => Err(PyValueError::new_err(format!("Internal conversion error: {}", regex_err))),
            }
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn _core(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(compilestr, module)?)?;
    Ok(())
}
