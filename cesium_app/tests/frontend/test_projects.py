import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import uuid
import time

from cesium_app.models import DBSession, Project


def test_create_project(driver):
    driver.get("/")

    # Add new project
    driver.wait_for_xpath('//*[contains(text(), '
                          '"Or click here to add a new one")]').click()

    project_name = driver.find_element_by_css_selector('[name=projectName]')
    test_proj_name = str(uuid.uuid4())
    project_name.send_keys(test_proj_name)
    project_desc = driver.find_element_by_css_selector('[name=projectDescription]')
    project_desc.send_keys("Test Description")

    driver.find_element_by_class_name('btn-primary').click()

    status_td = driver.wait_for_xpath(
        "//div[contains(text(),'Added new project')]")
    driver.refresh()

    proj_select = Select(driver.find_element_by_css_selector('[name=project]'))
    proj_select.select_by_visible_text(test_proj_name)
    time.sleep(0.1)

    assert driver.find_element_by_css_selector('[name=projectDescription]').\
        get_attribute("value") == "Test Description"

    # Delete project
    driver.find_element_by_partial_link_text('Delete Project').click()
    time.sleep(0.1)


def test_edit_project(driver, project):
    driver.refresh()
    proj_select = Select(driver.find_element_by_css_selector('[name=project]'))
    proj_select.select_by_value(str(project.id))
    project_name = driver.find_element_by_css_selector('[name=projectName]')
    project_name.clear()
    test_proj_name = str(uuid.uuid4())
    project_name.send_keys(test_proj_name)
    project_desc = driver.find_element_by_css_selector('[name=projectDescription]')
    project_desc.clear()
    project_desc.send_keys("New Test Description")
    driver.find_element_by_class_name('btn-primary').click()

    status_td = driver.wait_for_xpath(
        "//div[contains(text(),'Successfully updated project')]")
    assert driver.find_element_by_css_selector('[name=projectName]').\
        get_attribute("value") == test_proj_name
    assert driver.find_element_by_css_selector('[name=projectDescription]').\
        get_attribute("value") == "New Test Description"


def test_delete_project(driver, project):
    driver.refresh()
    proj_select = Select(driver.find_element_by_css_selector('[name=project]'))
    proj_select.select_by_value(str(project.id))
    driver.find_element_by_partial_link_text('Delete Project').click()
    status_td = driver.wait_for_xpath(
        "//div[contains(text(),'Project deleted')]")


def test_main_content_disabled_no_project(driver):
    Project.query.delete()
    DBSession.commit()
    driver.refresh()

    proj_select = Select(driver.find_element_by_css_selector('[name=project]'))
    try:
        proj_select.first_selected_option
    except NoSuchElementException:
        pytest.raises(WebDriverException, driver.find_element_by_id('react-tabs-2').click)
