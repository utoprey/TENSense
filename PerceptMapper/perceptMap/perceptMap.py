from logging import root
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty, BooleanProperty, DictProperty
from kivy.graphics import Color, Line
from kivy.uix.stencilview import StencilView
from kivy.uix.slider import Slider
# from threading import Thread
from kivy.uix.accordion import Accordion
from kivy.uix.popup import Popup
import yaml
import shutil
import os

import pandas as pd
import datetime
import sys


# try:
# 	from pylsl import resolve_streams, StreamOutlet, StreamInlet
# 	_PYLSL=True
# except Exception as e:
# 	print(e)
# 	_PYLSL=False


dictionary = str(input(print('Where to save?\n')))

""" # Это если слайдеры в опциональных
all_data = {'Data num' : [], 'Time' : [], 'coolSlider' : [],
            'electricSlider' : [], 'flutterSlider' : [],
            'itchSlider' : [], 'maintactileSlider' : [],
            'motorSlider' : [], 'naturalSlider' : [],
            'numbSlider' : [], 'painSlider' : [],
            'phantomSlider' : [], 'pressureSlider' : [],
            'prickSlider' : [], 'pulseSlider' : [],
            'sharpSlider' : [], 'shockSlider' : [],
            'tempSlider' : [], 'tickleSlider' : [],
            'tingleSlider' : [], 'touchSlider' : [],
            'urgeSlider' : [], 'vibrationSlider' : []}
"""

# Просто факт ощущния в опциональных
all_data = {'Picture' : [], 'Time' : [],
            'naturalSlider' : [], 'painSlider' : [], 'phantomSlider' : [],
            'motorSlider' : [], 'tempSlider' : [], 'maintactileSlider' : [],
            
            'Vibration' : [], 'Twitching' : [], 'Intention to Make Movement' : [],
            'Touch' : [], 'Squeezing' : [], 'Puncture' : [], 'Prickling' : [],
            'Electric Current' : [], 'Hit' : [], 'Pulsation' : [], 'Tickling' : [],
            'Itching' : [], 'Tingling' : [], 'Numbness' : [], 'Muscle contraction' : [],
            'Was Felt' : []}

# Чтобы переименовать
list_opt = [['Вибрация', 'Подергивание', "Намерение произвести движение",
              "Прикосновение", "Сдавливание", "Укол", "Покалывание",
              "Электрический ток", "Удар", "Пульсация", "Щекотка",
              "Зуд", "Пощипывание", "Онемение", "Сокращение мышцы"],
                
            ['Vibration', 'Twitching', "Intention to Make Movement",
             "Touch", "Squeezing", "Puncture", "Prickling",
             "Electric Current", "Hit", "Pulsation", "Tickling",
             "Itching", "Tingling", "Numbness", "Muscle contraction"]]

# Временный словарик для сбора факта нажатия кнопок
temp_dict = {'Вибрация' : False, 'Подергивание' : False, 'Намерение произвести движение' : False,
             'Прикосновение' : False, 'Сдавливание' : False, 'Укол' : False, 'Покалывание' : False,
             'Электрический ток' : False, 'Удар' : False, 'Пульсация' : False, 'Щекотка' : False,
             'Зуд' : False, 'Пощипывание' : False, 'Онемение' : False, 'Сокращение мышцы' : False}

def add_info(dicti, num):
    
    '''
    keys = dicti.keys()
    for key in all_data.keys():
        if key in keys:
            all_data[key].append(dicti[key])
        else:
            if key not in ['Picture', 'Time']:
                all_data[key].append('')
    '''
    
    keys = dicti.keys()
    for key in all_data.keys():
        if key in keys:
            all_data[key].append(dicti[key])
    
    all_data['Picture'].append(num)
    all_data['Time'].append(datetime.datetime.now().strftime('%H:%M:%S'))
    
    # ЧекБокс:
    print(f"all_data: {all_data}")
    print(f"temp_dict: {temp_dict}")
    for key in temp_dict.keys():
        key_s = list_opt[1][list_opt[0].index(key)]
        all_data[key_s].append(temp_dict[key])
    
    if all_data['motorSlider'][-1] == 0 or all_data['maintactileSlider'][-1] == 0:
        all_data['Was Felt'].append(False)
    else:
        all_data['Was Felt'].append(True)
        
        
    

class UserResponse(BoxLayout):
    """Main Kivy app class

    Contains the root widget that is updated after every user interaction, along with methods to save and reset the GUI.
    This app can also be run in auto-mode where file save and resset can be triggered by an external command. Pseudocode
    to set this up is included.
    """
    
    rootPath = StringProperty()
    repNumber = NumericProperty(0)
    sensationNumber = NumericProperty(0)
    saveFolder = StringProperty(dictionary)
    responseAnnot = set()

    def __init__(self, inputroot, imgfiles, tablabels, lastRep, mmm_ip, **kwargs):
        """
        Parameters
        ----------
        inputroot : str
            filepath where output files will be saved
        imgfiles:
            list of pngs to use for tabbed panel canvas
        tablabels:
            labels for tabs describing image
        lastRep:
            counter for the last trial
        mmm_ip : str
            IP address of message server machine (if using auto-mode)
        """

        super(UserResponse, self).__init__(**kwargs)
        self.rootPath = inputroot
        self.imgfiles = imgfiles
        self.repNumber = lastRep
        for idx, tabImg in enumerate(zip(imgfiles, tablabels)):
            self.ids['img%d' % idx].source = '../ImageBank/%s.png' % tabImg[0]
            self.ids['img%d' % idx].imglabel = tabImg[0]
            # self.ids['tab%d' % idx].text = tabImg[1]

        self.ids['frameLabel']._label._text = 'Кадр: '+str(self.repNumber)

        # PLACEHOLDER: connect to message server, subscribe to messages
        # PLACEHOLDER: start listener thread
        # self.listener=Thread(target=self.pyConsumer)
        # self.listener.daemon=True
        # self.listener.start()
        # print ("Consumer running...\n")
        
    def csv(self):
        fname = os.path.join(self.rootPath, self.saveFolder, self.saveFolder)
        pd.DataFrame(all_data).to_csv(fname+'_allData.csv', index=False)
        pd.DataFrame(all_data).to_excel(fname+'_allData.xlsx', index=False)
    
    def save_data(self):
        """Saves radiobutton, checkbox and slider values entered by user to a yml file in the specified location"""

        self.ids['responseAcc'].copy_accordion()

        fname = os.path.join(self.rootPath, self.saveFolder, self.saveFolder+"_R%03d" % self.repNumber)
        radiosliderdict = self.ids['responseAcc'].labelCheckDict.copy() #Сюда встравляются значения слайдера
        sensationdict = self.ids['floatStencilArea'].lineDict.copy() #Сюда похоже заносится все что нарисовано
        movedirdict = self.ids['floatStencilArea'].moveDict.copy()
        imgpropertiesdict = {'size': list(self.ids['img0'].get_norm_image_size()), 'pos': list(self.ids['img0'].pos)}

        if sensationdict or radiosliderdict['Sensation0']:
            if not (self.saveFolder in self.responseAnnot):
                self.responseAnnot.add(self.saveFolder)

            if not os.path.exists(os.path.join(self.rootPath, self.saveFolder)):
                    os.makedirs(os.path.join(self.rootPath, self.saveFolder))

            if sensationdict:
                with open(fname+'_imPixel.yml', 'w') as outfile:
                    outfile.write(yaml.dump(imgpropertiesdict, default_flow_style=False))
                    outfile.write(yaml.dump(sensationdict, default_flow_style=False))
                self.ids['floatStencilArea'].lineDict.clear()
            

                #for idx, tabImg in enumerate(zip(imgfiles, tablabels)):
                #    self.ids['img%d' % idx].source = '../ImageBank/%s.png' % tabImg[0]
                #    self.ids['img%d' % idx].imglabel = tabImg[0]
                #    self.ids['tab%d' % idx].text = tabImg[1]

            if radiosliderdict['Sensation0']:
                with open(fname+'_RadioCheckSlider.yml', 'w') as outfile:
                    outfile.write(yaml.dump(radiosliderdict, default_flow_style=False))
                    self.ids['responseAcc'].labelCheckDict.clear()
                # Правки Михаила Кнышенко -- нормальное выделение результатов
                print(f'radiosliderdict:\n {radiosliderdict["Sensation0"]}\n')
                add_info(radiosliderdict["Sensation0"], self.repNumber)
                
                '''
                for key in radiosliderdict["Sensation0"].keys():
                    all_data[key].append(radiosliderdict["Sensation0"][key])
                all_data['Number'].append(self.repNumber)
                '''

    def clear_window_canvas(self):
        """Clears all drawn lines on the image canvas"""

        for idx in range(len(self.imgfiles)):
            self.ids['img%d' % idx].clear_drawn_lines('all')

    def reset_radio_check_slider(self):
        """resets radiobutton, checkbox and slider values"""

        self.ids['qualityAccordion'].collapse = False
        self.ids['modalityAccordion'].collapse = True
        for widg in self.ids.keys():            # this is slightly uncouth
            if 'Box' in widg:
                self.ids[widg].set_labels_and_radio(False)
        for iKey in ['naturalSlider', 'painSlider', 'phantomSlider', 'motorSlider','tempSlider','maintactileSlider']:

            if iKey in ['naturalSlider', 'painSlider','tempSlider', 'phantomSlider' ]:
                self.ids[iKey].value = 0
            else:
                self.ids[iKey].value = 5
            self.ids[iKey].cursor_image = '../ImageBank/sliderVal.png'

            slider_ = self.ids[iKey]
            # https://stackoverflow.com/questions/66350205/how-to-simulate-user-action-on-kivy-widget-click-on-a-button-by-example
            from kivy.input.providers.mouse import MouseMotionEvent
            touch = MouseMotionEvent(None, 123, (123, 456))  # args are device, id, spos
            touch.button = 'left'
            touch.pos = slider_.value_pos
            touch.grab_current=slider_
            slider_.dispatch('on_touch_up', touch)


        #for i in self.ids['depthbox1'].children:
        #    i.active=False
        #for i in self.ids['depthbox2'].children:
        #    i.active = False
        #for i in self.ids['PLPbox1'].children:
        #    i.active=False
        #for i in self.ids['PLPbox2'].children:
        #    i.active = False

        pass

    # PLACEHOLDER: listener function
    # def pyConsumer(self):
    #    """Runs an infinite while loop to listen to subscribed messages and trigger GUI events when run in auto-mode"""
    #     disableScreen=Popup(opacity = 0.8, auto_dismiss = False, title = 'RESPONSES DISABLED', title_align = 'center')
    #     disableScreen.open()
    #     time.sleep(0.5)
    #
    #     while (1):
    #         non-blocking read of every subscribed message
    #         if TRIAL_START
    #               set self.saveFolder name
    #               reset counters
    #               disable popup
    #               play tone
    #
    #         elif STIM_END
    #               dismiss popup/enable GUI
    #
    #         elif TRIAL_END
    #             self.save_data()
    #             Clock.schedule_once(lambda dt: self.ids["imageTab"].switch_to(self.ids["imageTab"]._original_tab))
    #             Clock.schedule_once(lambda dt: self.clear_window_canvas())
    #             Clock.schedule_once(lambda dt: self.reset_radio_check_slider())
    #             Clock.schedule_once(lambda dt: disableScreen.open())
    #
    #         time.sleep(0.001)
    #     pass


class FrameLabel(Button):
    def __init__(self, **kwargs):
        super(FrameLabel, self).__init__(**kwargs)


class SaveResetButton(Button):
    """Triggers file save and GUI reset when GUI is run in manual-mode

    comment this class if running in auto mode
    """

    def __init__(self, **kwargs):
        super(SaveResetButton, self).__init__(**kwargs)

    def on_press(self):
        """Button callback to save data and reset GUI"""

        rootwidget = self.get_root_window().children[-1]
        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']
        rootwidget.save_data()
        rootwidget.clear_window_canvas()

        imgfiles=['Rpalmar', 'Rdorsum', 'Farms', 'Barms', 'Lpalmar', 'Ldorsum']
        tablabels= ['Right\nPalm', 'Right\nDorsum', 'Arms\nFront', 'Arms\nBack', 'Left\nPalm', 'Left\nDorsum']

        for idx, tabImg in enumerate(zip(imgfiles, tablabels)):
            rootwidget.ids['img%d' % idx].source = '../ImageBank/%s.png' % tabImg[0]
            #self.ids['img%d' % idx].imglabel = tabImg[0]
            #self.ids['tab%d' % idx].text = tabImg[1]

        #for idx in  range(len(['Barms','Farms','Ldorsum','Lpalmar','Rdorsum','Rpalmar'])):

        #    try:
        #        rootwidget.ids['img%d' % idx].source ='../ImageBank/%s.png' % tabImg[0]

        #        self.ids['img%d' % idx].source = '../ImageBank/%s.png' % tabImg[0]
        #    except:
        #        print('No', i)

        rootwidget.reset_radio_check_slider()
        rootwidget.repNumber += 1
        rootwidget.ids['frameLabel']._label._text = 'Кадр: ' + str(rootwidget.repNumber)
        rootwidget.ids['frameLabel']._trigger_texture()
        # import pdb; pdb.set_trace()
        rootwidget.sensationNumber = 0
        rootwidget.ids["imageTab"].switch_to(rootwidget.ids["imageTab"]._original_tab)
        # prevent propagation of touch
        stencilobj.buttonPress = True
        return True

# Дописанная с нуля    
class CloseButton(Button):
    """Triggers file save and GUI reset when GUI is run in manual-mode

    comment this class if running in auto mode
    """

    def __init__(self, **kwargs):
        super(CloseButton, self).__init__(**kwargs)

    def on_press(self):
        """Button callback to close window and save data"""

        rootwidget = self.get_root_window().children[-1]
        rootwidget.csv()
        App.get_running_app().stop()
        Window.close() 


class ResponseAccordion(Accordion):
    """Accordion containing descriptors for quality and modality

    """

    tempDict = DictProperty({})               # flushed after each sensation
    labelCheckDict = DictProperty({})

    def __init__(self, **kwargs):
        super(ResponseAccordion, self).__init__(**kwargs)
        
    def copy_accordion(self):
        """copies user responses from widget to temporary dictionary

        """

        sensekey = 'Sensation'+str(self.get_parent_window().children[-1].sensationNumber)
        responseaccobj = self.get_parent_window().children[-1].ids['responseAcc']

        responseaccobj.labelCheckDict[sensekey] = responseaccobj.tempDict.copy()
        responseaccobj.tempDict.clear()


class LabelCheckResponse(CheckBox, Label):
    """class for checkbox/radio button with associated text

    """
    descriptors = ListProperty()

    def __init__(self, **kwargs):
        super(LabelCheckResponse, self).__init__(**kwargs)
        self.descriptors = ["Vibration", "Flutter", "Buzz", "Urge to move", "Touch", "Pressure", "Sharp", "Prick", "Tap",
                            "Electric current", "Shock", "Pulsing", "Tickle", "Itch", "Tingle", "Numb", "Warm", "Cool"]

    def on_touch_up(self, touch):
        """enables checkbox/radiobutton

        """
        
        if touch.grab_current == self:
            self.set_labels_and_radio(self.active)

    def set_labels_and_radio(self, isactive):
        """callback for radio or checkbox

        """
        # Добавочка
        text = self.text
        act = self.active
        temp_dict[text] = act
        print(self.text + ' enabled: ' + str(self.active))
        print(temp_dict)
        
        rootwidget = self.get_root_window().children[-1]

        if isactive:  # is active
            if not self.group:  # checkbox
                for responseObj in self.parent.children[:-1]:
                    responseObj.canvas.opacity = 1              # canvas of boxlayout
                    responseObj.disabled = False

                    # https://stackoverflow.com/questions/66350205/how-to-simulate-user-action-on-kivy-widget-click-on-a-button-by-example
                    from kivy.input.providers.mouse import MouseMotionEvent
                    touch = MouseMotionEvent(None, 123, (123, 456))  # args are device, id, spos
                    touch.button = 'left'
                    touch.pos = responseObj.center
                    touch.grab_current=responseObj
                    responseObj.dispatch('on_touch_up', touch)

                    #self.cursor_image = 'atlas://data/images/defaulttheme/slider_cursor'
                    # self.value_pos = touch.pos
                    #rootwidget.ids['responseAcc'].tempDict[self.id2] = round(self.value, 3)
                
                # Добавочка
                #print(self.text + ' enabled: ' + str(self.active))
                #text = self.text
                #act = self.active
                #temp_dict[text] = act
                #print(temp_dict)
                

            else:  # radiobox
                if self.active:  # 2 radio selections are detected as active. can be handled better by binding on_active
                    rootwidget.ids['responseAcc'].tempDict[self.group] = self.text
                    print(self.group + ' - ' + self.text + ' sensation')
                    # Добавочка
                    
                    #text = self.text
                    #act = self.active
                    #temp_dict[text] = act

                    # PLACEHOLDER: send message for selected radiobutton

        else:  # is inactive
            if not self.group:          # checkbox
                self.active = False
                #print(self.text + ' enabled: ' + str(self.active))
                #text = self.text
                #act = self.active
                #temp_dict[text] = act
                #print(temp_dict)
                
                for responseObj in self.parent.children[:-1]:
                    responseObj.canvas.opacity = 0   #canvas of boxlayout
                    responseObj.disabled = True
                    responseObj.value = 0    # slider
                    responseObj.cursor_image = '../ImageBank/sliderVal.png'
                    try:
                        del rootwidget.ids['responseAcc'].tempDict[responseObj.id2]
                    except Exception as e:
                        print(e)

                if self.group in rootwidget.ids['responseAcc'].tempDict.keys():
                    rootwidget.ids['responseAcc'].tempDict[self.group]=''
        
        


class SliderResponse(Slider):
    """class for all slider/intensity widgets

    """
    id = ObjectProperty(None)
    id2 = StringProperty('')
    modalityList = ListProperty()

    def __init__(self, **kwargs):
        super(SliderResponse, self).__init__(**kwargs)
        self.cursor_image = '../ImageBank/sliderVal.png'
        self.modalityList = ["Vibration", "Flutter", "Buzz", "Urge to move", "Touch", "Pressure", "Sharp", "Prick", "Tap",
                            "Electric current", "Shock", "Pulsing", "Tickle", "Itch", "Tingle", "Numb", "Warm", "Cool"]

    def on_touch_up(self, touch):
        rootwidget = self.get_root_window().children[0]
        if touch.grab_current == self:
            self.cursor_image = 'atlas://data/images/defaulttheme/slider_cursor'
            self.value_pos = touch.pos
            rootwidget.ids['responseAcc'].tempDict[self.id2] = round(self.value, 3)
            print(self.value)

            # PLACEHOLDER: send message for slider value


class SensationButton(Button):
    """2 rectangular buttons in bottom right corner

    all lines that are drawn on the current image are cleared when the clear button is pressed. when add sensation
    button is pressed, opacity of all lines is changed, these lines cannot be edited or cleared and the counter
    for sensation is incremented
    """

    id2 = StringProperty('')

    def __init__(self, **kwargs):
        super(SensationButton, self).__init__(**kwargs)

    def on_press(self):

        rootwidget = self.get_root_window().children[-1]
        responseaccobj = self.get_parent_window().children[-1].ids['responseAcc']
        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        cur_frame = rootwidget.repNumber

        if self.id2 == 'add':

            # copy current dictionary to accordion dictionary
            responseaccobj.copy_accordion()

            # set new color
            rootwidget.ids['imageTab'].children[1].children[0].paintbrush()

            # clear pointers to line objects from previous sensation
            rootwidget.ids['imageTab'].children[1].children[0].oldSegment_buffer.extend(rootwidget.ids['imageTab'].children[1].children[0].segment_color)
            rootwidget.ids['imageTab'].children[1].children[0].segment_color = []

            # clear all radio buttons
            self.get_parent_window().children[-1].reset_radio_check_slider()

            print('added sensation')

        else:  # clear lines button

            sensekey = 'sensation'+str(rootwidget.sensationNumber)+'_'+stencilobj.currImagename

            if sensekey in stencilobj.lineDict.keys():        # line has been drawn

                del stencilobj.lineDict[sensekey]       # delete pixel coordinates

                rootwidget.ids[stencilobj.currImage].clear_drawn_lines('currentSense')

            if sensekey in stencilobj.moveDict.keys():
                stencilobj.moveDict[sensekey] = []

            # rootwidget.reset_radio_check_slider()


        # prevent propagation of touch
        stencilobj.buttonPress = True
        return True


class RestoreButton(Button):
    id2 = StringProperty('')

    def __init__(self, **kwargs):
        super(RestoreButton, self).__init__(**kwargs)

    def on_press(self):

        rootwidget = self.get_root_window().children[-1]
        rootwidget.reset_radio_check_slider()

        try:    
            #rootwidget.ids[0].source = '../ImageBank/Rpalmar_.png'
            previous_value=rootwidget.repNumber-1
            print('Previous values equals to', previous_value)

            pics=['Rpalmar', 'Rdorsum', 'Farms', 'Barms', 'Lpalmar', 'Ldorsum']

            for i in range(len(pics)):
                pic_inst=pics[i]
                try:
                    if os.path.exists('../data/default/default_R' + str(previous_value) + '_'+pic_inst+'.png'):
                        rootwidget.ids['img'+str(i)].source = '../data/default/default_R' + str(previous_value) + '_'+pic_inst+'.png'
                        shutil.copyfile('../data/default/default_R' + str(previous_value) + '_'+pic_inst+'.png', 
                                        '../data/default/default_R' + str(rootwidget.repNumber) + '_'+pic_inst+'.png')
                except:
                    print('No picture', pic_inst)

            yaml_file_slider='../data/default/default_R' + str(previous_value) + '_RadioCheckSlider.yml'
            #default_R346_RadioCheckSlider.yml
            with open(yaml_file_slider, 'r') as stream:
                data_loaded = yaml.safe_load(stream)['Sensation0']

            yaml_file_image = '../data/default/default_R' + str(previous_value) + '_imPixel.yml'
            with open(yaml_file_image, 'r') as stream:
                image_data_loaded = yaml.safe_load(stream)#['Sensation0']

                #imgpropertiesdict = {'size': list(self.ids['img0'].get_norm_image_size()),
                #1: image_data_loaded['pos']: list(self.ids['img0'].pos)}
                #2: про сайз
                #3: sensationdict = self.ids['floatStencilArea'].lineDict.copy()

                #outfile.write(yaml.dump(imgpropertiesdict, default_flow_style=False))
                #outfile.write(yaml.dump(sensationdict, default_flow_style=False))

        except Exception as e:
            print(e)
            print('No previous value files')

        sensekey = 'Sensation 0'
        responseaccobj = self.get_parent_window().children[-1].ids['responseAcc']

        # responseaccobj.labelCheckDict= data_loaded
        for k, v in data_loaded.items():
            slider_ = rootwidget.ids.get(k, None)
            if slider_ is None:
                continue
            slider_.value = v
            responseaccobj.tempDict[k] = data_loaded[k]
            slider_.opacity=1
            slider_.disabled=False

            try:
                if len(slider_.parent.children)!=2:
                    continue
                chbox = slider_.parent.children[-1] # try to locate checkbox
                chbox.active = True
                print(chbox)
            except Exception as e:
                print(e)


        for i in  ['Barms','Farms','Ldorsum','Lpalmar','Rdorsum','Rpalmar']:
            try:
                rootwidget.ids['floatStencilArea'].lineDict['sensation0_'+i]=image_data_loaded['sensation0_'+i]
                print('Loaded', i)
            except:
                print('No', i)

        print('Data Loaded Successfully')


class FloatStencil(FloatLayout, StencilView):
    """Widget containing tabbed panel items and png images

    """

    lineDict = DictProperty()
    moveDict = DictProperty()
    buttonPress = BooleanProperty(False)
    currImage = StringProperty('img0')
    currImagename = StringProperty('')

    def __init__(self, **kwargs):
        super(FloatStencil, self).__init__(**kwargs)


class CustomImage(Image):
    """widget containing png images

    all lines are drawn on the canvas of this widget. Lines drawn in the movement popup are transferred to this canvas.
    The color of the line is based on the sensation number. The order of colors is stored in self.colors property. The
    default order of line colors is purple, cyan, green, red, blue, yellow, orange, pink, brown, aqua-green, magenta,
    orange-chalk, teal
    """

    colors = ListProperty()
    oldSegment_buffer = ListProperty()
    segment_color = ListProperty()
    moveSegment_color = ListProperty()
    id2 = StringProperty('')

    def __init__(self, **kwargs):
        super(CustomImage, self).__init__(**kwargs)
        self.colors = [[0.5, 0.00, 0.8], [0.16, 0.78, 0.88], [0.31, 0.63, 0.06], [0.95, 0.37, 0.39], [0.35, 0.35, 0.82],
                       [0.99, 0.90, 0.05], [0.93, 0.54, 0.14], [0.93, 0.24, 0.89], [0.64, 0.38, 0.00],
                       [0.12, 0.74, 0.48], [0.93, 0.18, 0.55], [0.98, 0.45, 0.37], [0.09, 0.22, 0.25]]

    def paintbrush(self):
        with self.canvas:
            for lineObj in self.segment_color:
                lineObj.a = 0.5
            self.get_parent_window().children[-1].sensationNumber += int(1)

    def on_touch_down(self, touch):

        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if self.collide_point(touch.x, touch.y):
            stencilobj.currImage = self.id2
            stencilobj.currImagename = self.imglabel
            stencilobj.buttonPress = False
            with self.canvas:
                self.segment_color.append(Color(*self.colors[int(self.get_parent_window().children[-1].sensationNumber % 13)]))
                touch.ud['line'] = Line(width=5, points=(touch.x, touch.y))
            return True

    def on_touch_move(self, touch):
        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if not stencilobj.buttonPress:
            if self.collide_point(touch.x, touch.y) and 'line' in touch.ud.keys():
                touch.ud['line'].points += [touch.x, touch.y]
                return True

    def on_touch_up(self, touch):

        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if not stencilobj.buttonPress:
            if self.collide_point(touch.x, touch.y):
                if 'line' in touch.ud.keys():

                    currentimg = stencilobj.currImagename
                    sensekey = 'sensation'+str(self.get_parent_window().children[-1].sensationNumber)+'_'+currentimg

                    if sensekey in stencilobj.lineDict.keys():
                        stencilobj.lineDict[sensekey] += touch.ud['line'].points
                    else:
                        stencilobj.lineDict[sensekey] = touch.ud['line'].points

                    self.save_png(0)

                    # PLACEHOLDER: send message with pixel coordinates
                    return True

                else:
                    return True

        else:
            stencilobj.buttonPress = False
            return True

    def clear_drawn_lines(self, lines):
        if lines == 'currentSense':               # clear latest drawn line.
            with self.canvas:
                for lineObj in self.segment_color:
                    lineObj.a = 0
            self.segment_color = []
        else:                                   # clear all lines
            with self.canvas:
                for lineObj in self.segment_color + self.oldSegment_buffer:
                    lineObj.a = 0
            self.segment_color = []

    def save_png(self, child_idx):
        rootwidget = self.get_parent_window().children[child_idx]
        if not os.path.exists(os.path.join(rootwidget.rootPath, rootwidget.saveFolder)):
            os.makedirs(os.path.join(rootwidget.rootPath, rootwidget.saveFolder))

        self.export_to_png(os.path.join(rootwidget.rootPath, rootwidget.saveFolder,
                                        rootwidget.saveFolder+"_R%03d" % rootwidget.repNumber+'_'+self.imglabel+'.png'))


class PerceptMap(App):
    """perceptmap app class

    if a perceptmap.ini file does not exist it will be created in the same folder with the dfault parameters specified in
    build_config. edit the *.ini file to change these parameters
    """
    
    def build_config(self, config):
        config.setdefaults('config', {
            'savePath': dictionary,
            #'savePath': '../data',
            'mmip': 'localhost',
            'windowSize': (1368, 912),
            'windowColor': (1, 1, 1, 1),
            'windowBorderless': False,
            'imgFiles': ['Rpalmar', 'Rdorsum', 'Farms', 'Barms', 'Lpalmar', 'Ldorsum'],
            'tabLabels': ['Rpalmar', 'Rdorsum', 'Farms', 'Barms', 'Lpalmar', 'Ldorsum'],
            #'tabLabels': ['Right\nPalm', 'Right\nDorsum', 'Arms\nFront', 'Arms\nBack', 'Left\nPalm', 'Left\nDorsum'],
            'trialNumber': 0
        })

    def build(self):
        config = self.config
        Window.size = eval(config.get('config', 'windowSize'))
        Window.clearcolor = eval(config.get('config', 'windowColor'))
        Window.borderless = config.getboolean('config', 'windowBorderless')
        Window.maximize()
        if not os.path.exists(config.get('config', 'savePath')):
            os.makedirs(config.get('config', 'savePath'))
        return UserResponse(config.get('config', 'savePath'), eval(config.get('config', 'imgFiles')),
                            eval(config.get('config', 'tabLabels')), int(config.get('config', 'trialNumber')),
                            config.get('config', 'mmip'))

    def on_stop(self):
        config = self.config
        #config.set('config', 'trialNumber', self.root_window.children[-1].repNumber)
        #config.write()

    def on_start(self, *args, **kwargs):
        self.root.reset_radio_check_slider()




if __name__ == '__main__':
    #dictionary = '../data/' + str(input(print('Where to save?\t')))
    PerceptMap().run()
