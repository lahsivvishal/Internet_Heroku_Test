import pytest
from frontEndAssignment import FrontEndAssignment
fae = FrontEndAssignment()

def test_broken_image():
    result = fae.imageComposureCheck()
    assert result == True

def test_forgotPassword():
    result = fae.forgotPassword()
    assert result == True

def test_FormValidation_wrongCreds():
    result = fae.formValidationWrongCreds()
    assert result == False

def test_formValidation_RightCreds():
    result = fae.formValidationRightCreds()
    assert result == True

def test_charInput():
    result = fae.charInput()
    assert isinstance(result, int)

def test_table_sort():
    result1 = fae.tableSort('table1')
    assert result1 == True
    result2 = fae.tableSort('table2')
    assert result2 == True

def test_notification():
    result = fae.notification()
    assert result == True
