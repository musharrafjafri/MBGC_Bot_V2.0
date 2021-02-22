from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from tableData import table_data_func as tdf
from selenium.webdriver.chrome.options import Options
from time_list import time_list_fun as tlf

# options = webdriver.ChromeOptions()
# options.add_argument('start-maximized')
# options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# driver = webdriver.Chrome(options=options)
# driver.maximize_window()


# In this function Chrome driver loaded in driver and clicked on Agree button.
def driver_fun():
    driver.get('https://booking.mbgc.com.sg/')
    sleep(1)
    driver.find_element_by_link_text('I Agree').click()


# In this function today date picked for next functions.
def current_date_fun(num=0):
    sleep(1)
    driver.find_element_by_class_name('date_picker').click()
    c_date = driver.find_element_by_class_name('ui-datepicker-today').text
    c_date = int(c_date) + num
    c_date = str(c_date)
    return c_date


# It is used when month is end and BOT goes to next month for pickup the dates.
def next_month_fun():
    driver.find_element_by_xpath('/html/body/div[10]/div/a[2]').click()  # click on calendar
    date_picker = driver.find_element_by_class_name('ui-datepicker-calendar')  # take date picker
    tags_text = []
    desire_last_date = ''
    for tags in date_picker.find_elements_by_tag_name('a'):  # Finding all a tags in calendar's div
        tags_text.append(tags.text)  # Append a tag's texts

    desire_last_date = tags_text.pop() # get the last a tag which is our 15+ desire date
    for row in range(1, 6):  # take all calendar's rows
        for column in range(1, 8):  # take all calendar's column
            if driver.find_element_by_xpath(f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{row}]/td[{column}]').text == desire_last_date:  # Maching the last a tag we got above with calendar's texts
                driver.find_element_by_xpath(f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{row}]/td[{column}]').click()  # click on the matched a tag which will be our 15+ date in next month.


# This function used to get desire date which 15+ date in current month if next month is not applicable.
def desire_date_fun():
    c_row = 0
    c_column = 0
    c_date = current_date_fun()
    for row in range(1, 6):  # take all calendar's rows
        for column in range(1, 8):  # take all calendar's column
            current_date_pos = driver.find_element_by_xpath(
                f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{row}]/td[{column}]').text  # Taking current date to calculate 15+ date further
            if current_date_pos == c_date:  # Matching the current date with current position to know row and column for current date.
                table_data = tdf(row, column)  # Getting table_data from table_data_function from another module and gave them row and column data to calculate 15+ date's row and column.
                c_row = table_data[0]  # Getting 15+ date's row data
                c_column = table_data[1]  # Getting 15+ date's column data
    desire_date = driver.find_element_by_xpath(f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{c_row}]/td[{c_column}]')  # now we got our desire date's row and column to move ahead for current month.
    # Try function is used to check the desire date is in the current month or we should call the next month.
    is_date_avail = False
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{c_row}]/td[{c_column}]/a'))
        )
        is_date_avail = True  # If desire date's row and column data is in the current month than True tha is_data_avail.
        desire_date.click()
    except:
        is_date_avail = False  # If desire date's row and column data is not in the current month than False tha is_data_avail to go to next month functions.
    return is_date_avail


# It use for know if courses or desire course is available or not.
def is_course_available_fun():
    is_avail = False
    desire_course = False
    # try function is used here for check if Available courses is available or not.
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="AvailCourse"]/a'))
        )
        courses = driver.find_element_by_id('AvailCourse')
        # Now if courses available so our desire course "Day Golf (18 Holes)" is available or not.
        for course in courses.find_elements_by_tag_name('a'):
            if course.text == "Day Golf (18 Holes)":
                course.click()
                print(">>>>>CONGRATS, DAY GOLF (18 HOLES) IS AVAILABLE...")
                desire_course = True
                break
            else:
                desire_course = False
        return desire_course
    except:
        is_avail = False

    if desire_course:
        is_avail = True
    else:
        is_avail = False

    return is_avail


# It is used to know if our desire time is not on hold.
def is_time_hold_fun():
    desire_time_ids = times_fun()  # Getting all desire time ids from time_fun.
    time_tree = driver.find_element_by_id('divTee')  # Taking all times which are available on page.
    hold_flag = True
    booked_time = None
    incompl_flag = True
    # while function runs until unhold date is not available.
    while hold_flag:
        for i in range(1, 2): # run for loop for once.
            for time_slot in time_tree.find_elements_by_tag_name('a'):  # taking all timeslot's a tag
                if time_slot.get_attribute('data-tee-time') in desire_time_ids:  # checkif timeslot's id is matched with our desire time ids.
                    if time_slot.get_attribute('class') != 'ui button slots tee-time golfer_book holdGolfer':  # If it above statement matched than checked if it is not hold.
                        booked_time = time_slot.get_attribute('data-tee')  # Here we get our booked time which is booked by this function it used only for print to know what time is it.
                        print(">>>>>Selected time is: ", booked_time, " proceed with Player's detail...")  # Here we print the booked time.
                        element_to_hover_over = time_slot  # now in next three lines we use hover function to visible book button.
                        hover = ActionChains(driver).move_to_element(element_to_hover_over)
                        hover.perform()
                        time_slot.click()  # Now finally we're clicking on th Book button.
                        sleep(3)  # wait for 3 seconds to load page fully.
                        driver.find_element_by_xpath('/html/body/section/form/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/input').click()  # Clicking on the "Proceed as guest" button.
                        incompl_flag = False  # now false this flag to stop loop to getting desire time.
                        hold_flag = False  # now false this flag to stop loop to wait for unhold timeslot.
                        break
                    else:
                        incompl_flag = True  # True this flag to continue loop to getting desire time.
                        hold_flag = True  # True this flag to continue loop to wait for unhold timeslot.
    return incompl_flag


# In this function we getting time's ids and times to used in above functions.
def times_fun():
    time_tree = driver.find_element_by_id('divTee')
    times_and_ids_dict = {}
    for time_tags in time_tree.find_elements_by_tag_name('a'):
        times_and_ids_dict.update({time_tags.get_attribute('data-tee'): time_tags.get_attribute('data-tee-time')})

    time_list_fun = tlf()
    dict_times = times_and_ids_dict.keys()
    dict_times_list = list(dict_times)
    desire_time_ids = []
    for i in range(len(dict_times_list)):
        if dict_times_list[i] in time_list_fun:
            desire_time_ids.append(times_and_ids_dict.get(dict_times_list[i]))
    return desire_time_ids



# This is main function in which all function call for process the BOT
def main_fun():
    global booked_flag
    for dr_num in range(2):
        try:
            driver_fun()  # Load the driver and click on Agree Button.
            print(">>>>>Driver loaded...")
            break
        except:
            print(">>>>>Waiting for driver to load")

    sleep(1)

    for dd_num in range(2):
        try:
            if desire_date_fun():  # If date is available in current month than just click on that desire date.
                pass
            else:  # If date is not in current month than run the next month function.
                next_month_fun()
            break
        except:
            print(">>>>>There is a problem in date function, trying to fix it please wait...")

    for c_num in range(2):
        try:
            print(">>>>>TRYING TO FIND COURSE, PLEASE WAIT...")  # Printing this line until find the desire course.
            while is_course_available_fun() == False:  # Run this loop while courses appear on page or our specific (Day Golf (18 Holes) course.
                driver.refresh()  # refresh page and run funcitons agian.
                sleep(1)
                if desire_date_fun():  # If date is available in current month than just click on that desire date.
                    pass
                else:  # If date is not in current month than run the next month function.
                    next_month_fun()
                is_course_available_fun()
            break
        except:
            print(">>>>>There is a problem in course function, trying to fix it please wait...")

    sleep(1)
    for d_num in range(2):
        try:
            desire_time_id = times_fun()  # get desire time ids that is available or not.
            if desire_time_id != []:  # If desire time ids is not Null than move ahead
                print(">>>>>TRYING TO FIND TIMSLOT WHICH IS NOT BOOKED, PLEASE WAIT...")
                time_hold_flag = is_time_hold_fun()  # Run hold time function.
                # while time_hold_flag:  # if desire time is on hold than run this loop until find the timeslot unhold.
                #     print(">>>>>TRYING TO FIND TIMSLOT WHICH IS NOT BOOKED, PLEASE WAIT...")  # print this line until timeslot unhold.
                #     times_fun()  # run time function again.
                #     is_time_hold_fun()  # check if time is still on hold or it is ready for book.
            else:
                print(">>>>>There is no timeslot available between 07:00 to 13:00, Try again later...")  # if desire time is not availble in all timeslots than print this line.
                driver.execute_script("window.alert('There is no timeslot available between 07:00 to 13:00, Try again later...');")  # if desire time is not availble in all timeslots than this popup message show on browser.
            if not time_hold_flag:
                booked_flag = True
            break
        except:
            print(">>>>>There is a problem in timeslot function, trying to fix it please wait...")

    if not booked_flag:
        driver.quit()

time1 = input()

print("--------------------->>>>>>>>>><<<<<<<<<<----------------------")
print(">>>>>BOT IS STARTING...")
booked_flag = False
while not booked_flag:
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument("--log-level=3")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    main_fun()  # Run main function to execute BOT.

print(">>>>>BOT stopped...")
print("--------------------->>>>>>>>>><<<<<<<<<<----------------------")
