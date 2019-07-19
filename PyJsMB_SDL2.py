#!/usr/bin/python
# coding: utf-8

import ctypes
import math
import sdl2 as SDL

# Heavily modified JsMB-SDL2 Alpha 11 58884391d121876a2269f10202c65a9761b25e78

class JsMB():
    Mouse = {
        'x': 0,
        'y': 0,
        'lcount': 0,
        'rcount': 0
    }

    Gel = { 'Sprite': {} }
    
    Font = {
        'family': 'arial',
        'size': '10'
    }

    Draw = {
        'color': None,
        'BGCOLOR': [255, 255, 255, 255],
        'linewidth': 1
    }

    JsMobileBasic = {
        'name': 'JsMobileBasic',
        'version': 'Alpha 11',
        'author': 'PROPHESSOR',
        'url': 'http://vk.com/JsMobileBasic',
        'Mobile': None, # Config.Mobile,
        'Debug': True,
        'canvas': None, # typeof document === 'undefined' ? null : document.getElementById('c'),
        'graphics': True,
        'supports': {
            'document': False,
            'window': False,
            'browser': False,
            'ls': False,
            'module': False
        }
    }

    Instance = {
        'name': 'JsMobileBasic'
    }

    PI = math.pi,
    G = 9.8 # TODO: DEPRECATE
    RAD2DEG = 180 / math.pi
    DEG2RAD = math.pi / 180

    def __init__(self, config=None, canvas=None, renderer=None, main=None, loop=None):
        # TODO:
        self.SCW = 640
        self.SCH = 480

        self.debug('#===== Включён режим отладки =====#', 'color:gray;')
        self.debug(self.JsMobileBasic['name'], 'background:gray;color:yellow;')
        self.debug('v. ' + self.JsMobileBasic['version'], 'background:gray;color:yellow;')
        self.debug('by ' + self.JsMobileBasic['author'], 'background:gray;color:yellow;')
        self.debug(self.JsMobileBasic['url'], 'background:gray;color:yellow;')

        self.debug('// ======Инициализация рабочей среды======//', 'color:gray;')


        if config:
            if 'name' in config:
                self.Instance['name'] = config['name']

            if 'Debug' in config:
                self.JsMobileBasic['Debug'] = config['Debug']


        self.debug('Используется графика!', 'background:black;color:yellow;')

        # TODO: Read screen size from config
        self.JsMobileBasic['canvas'] = self.c = canvas if canvas else SDL.SDL_CreateWindow(bytes(self.Instance['name'], 'utf-8'), SDL.SDL_WINDOWPOS_UNDEFINED, SDL.SDL_WINDOWPOS_UNDEFINED, self.SCW, self.SCH, SDL.SDL_WINDOW_SHOWN)

        # TODO: SDL_WINDOW_FULLSCREEN

        self.ctx = renderer if renderer else SDL.SDL_CreateRenderer(self.c, -1, SDL.SDL_RENDERER_ACCELERATED | SDL.SDL_RENDERER_PRESENTVSYNC)

        self.setLineWidth(1)
        self.setColor([255, 0, 0, 0])
        self.fillScreen(255, 255, 255, 255)
        self.repaint()

        self.debug('Имя проекта: ' + self.Instance['name'], 'background:brown;color:yellow;')

        self.Player = [None]

        self.debug('// ======Инициализация интерпретатора======//', 'color:gray;')

        self._main = main
        self._loop = loop

        if self._main:
            self._main(self)

        event = SDL.SDL_Event()

        running = True

        while running:
            while SDL.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL.SDL_QUIT:
                    running = False
                    break

            if self._loop:
                self._loop(self) # TODO: Send keycode

        SDL.SDL_DestroyRenderer(self.ctx)
        SDL.SDL_DestroyWindow(self.c)
        SDL.SDL_Quit()

    @classmethod
    def Debug(*args):
        print(*args)

    def debug(self, *args):
        if self.JsMobileBasic['Debug']:
            print(*args)

    def setColor(self, *color):
        ''' Задать текущий цвет
        * @param  {array} color - Цвет в RGB формате
        * @returns {self}
        '''
        if len(color) == 1: color = color[0]

        cl = Color(color)
        self.Draw['color'] = cl

        SDL.SDL_SetRenderDrawColor(self.ctx, *cl.getRgbaArray())

        return self

    def setLineWidth(self, width):
        ''' Задать толщину линий
        * @param  {number} width - Толщина
        * @returns {self}
        '''
        self.Draw['linewidth'] = width
        return self

    def delay(self, ms):
        ''' Задержка в ms
        * @returns {self}
        '''
        SDL.SDL_Delay(ms)
        return self

    def cls(self):
        ''' Очищает экран
        * @returns {self}
        '''
        tmp = self.Draw['color']

        self.setColor(255, 255, 255, 255)
        SDL.SDL_RenderClear(self.ctx)
        self.setColor(tmp)

        return self

    def repaint(self):
        ''' Производит отрисовку на экран ранее произведенных действий
        * В стандартной реализации ничего не делает
        * @returns {self}
        '''
        SDL.SDL_RenderPresent(self.ctx)

        return self

    def drawPlot(self, x, y):
        ''' Рисует точку по координатам (заливает пиксель)
            * @param  {number} x - X координата точки
            * @param  {number} y - Y координата точки
            * @returns {self}
        '''
        pass # TODO:

    def drawLine(self, x1, y1, x2, y2):
        ''' Рисует линию по 2 точкам
         * @param  {number} x1 - X 1 точки
         * @param  {number} y1 - Y 1 точки
         * @param  {number} x2 - X 2 точки
         * @param  {number} y2 - Y 2 точки
         * @returns {self}
        '''
        SDL.SDL_RenderDrawLine(self.ctx, int(x1), int(y1), int(x2), int(y2))
        return self

    def drawRect(self, x, y, w, h):
        ''' Рисует прямоугольник
        * @param  {number} x - Координата X левого верхнего угла
        * @param  {number} y - Координата Y левого верхнего угла
        * @param  {number} w - Ширина
        * @param  {number} h - Высота
        * @returns {self}
        '''
        rect = SDL.SDL_Rect(int(x), int(y), int(w), int(h))

        SDL.SDL_RenderDrawRect(self.ctx, rect)

        return self

    def fillRect(self, x, y, w, h):
        ''' Рисует залитый прямоугольник
        * @param  {number} x - Координата X левого верхнего угла
        * @param  {number} y - Координата Y левого верхнего угла
        * @param  {number} w - Ширина
        * @param  {number} h - Высота
        * @returns {self}
        '''
        rect = SDL.SDL_Rect(int(x), int(y), int(w), int(h))

        SDL.SDL_RenderDrawRect(self.ctx, rect)
        SDL.SDL_RenderFillRect(self.ctx, rect)

        return self

    def fillScreen(self, *color):
        ''' Заливает экран выбранным цветом
        * @param  {string} color - Цвет в CSS формате
        * @returns {self}
        '''
        cl = self.Draw['color']

        self.setColor(color)
        self.fillRect(0, 0, self.screenWidth(), self.screenHeight())
        self.setColor(cl)


    # Getters
    def screenWidth(self):
        ''' Возвращает ширину экрана
        * @returns {number}
        '''

        return self.SCW

    def screenHeight(self):
        ''' Возвращает высоту экрана
        * @returns {number}
        '''

        return self.SCH

#     ''' Переключить полноэкранный режим
#      * @param  {bool} mode - True - включить, False - отключить
#      * @returns {self}
#     '''
#     fullScreen(mode) {
#         if (self.JsMobileBasic.supports.document) {
#             if (mode) {
#                 if (document.documentElement.requestFullscreen)
#                     document.documentElement.requestFullScreen()
#                 else if (document.documentElement.webkitRequestFullScreen)
#                     document.documentElement.webkitRequestFullScreen()
#             } else {
#                 if (document.cancelFullScreen)
#                     document.cancelFullScreen()
#                 else if (document.webkitCancelFullScreen)
#                     document.webkitCancelFullScreen()
#             }
#             return self
#         }
#         self.debug('Работа в полноэкранном режиме невозможна!')
#         return False
#     },

#     ''' Заливает экран выбранным цветом
#      * @param  {string} color - Цвет в CSS формате
#      * @returns {self}
#     '''
#     fillScreen(color) {
#         const tmp = self.ctx.color
#         self.setColor(color)
#         self.fillRect(0, 0, self.screenWidth(), self.screenHeight())
#         self.ctx.color = tmp
#         return self
#     },

#     ''' Рисует прямоугольник
#      * @param  {number} x - Координата X левого верхнего угла
#      * @param  {number} y - Координата Y левого верхнего угла
#      * @param  {number} w - Ширина
#      * @param  {number} h - Высота
#      * @returns {self}
#     '''
#     drawRect(x, y, w, h) {
#         self.ctx.drawRect([x, y, x1, y1])
#         return self
#     },

#     ''' Рисует точку по координатам (заливает пиксель)
#      * @param  {number} x - X координата точки
#      * @param  {number} y - Y координата точки
#      * @returns {self}
#     '''
#     drawPlot(x, y) {
#         self.ctx.drawPoint([[x, y]])
#         return self
#     },

#     ''' Очищяет прямоугольную область
#      * @param  {number} x - Координата X левого верхнего угла
#      * @param  {number} y - Координата Y левого верхнего угла
#      * @param  {number} w - Ширина
#      * @param  {number} h - Высота
#      * @returns {self}
#     '''
#     clearRect(x, y, w, h) {
#         const tmp = self.ctx.color
#         self.setColor(self.Draw.BGCOLOR)
#         self.fillRect(x, y, w, h)
#         self.ctx.color = tmp
#         return self
#     },

#     ''' Рисует линию по 2 точкам
#      * @param  {number} x1 - X 1 точки
#      * @param  {number} y1 - Y 1 точки
#      * @param  {number} x2 - X 2 точки
#      * @param  {number} y2 - Y 2 точки
#      * @returns {self}
#     '''
#     drawLine(x1, y1, x2, y2) {
#         if(x1 === Infinity || x2 === Infinity || y1 === Infinity || y2 === Infinity) return self
#         self.gfx.line(x1, y1, x2, y2, self.Draw.color.getNumber(), self.Draw._lineWidth)
#         return self
#     },

#     ''' Рисует проекцию паралелепипеда (через 2 соединенных прямоугольника)
#      * @param  {number} x - X левого верхнего угла
#      * @param  {number} y - Y левого верхнего угла
#      * @param  {number} w - ширина
#      * @param  {number} h - высота
#      * @param  {number} q - глубина
#      * @returns {self}
#     '''
#     drawCube(x, y, w, h, q) {
#         self.ctx.strokeRect(x, y, w, h)
#         self.ctx.strokeRect(x + (q / Math.sqrt(2)), y + (q / Math.sqrt(2)), w, h)
#         self.drawLine(x, y, x + (q / Math.sqrt(2)), y + (q / Math.sqrt(2)))
#         self.drawLine(x + w, y, x + w + (q / Math.sqrt(2)), y + (q / Math.sqrt(2)))
#         self.drawLine(x, y + h, x + (q / Math.sqrt(2)), y + h + (q / Math.sqrt(2)))
#         self.drawLine(x + w, y + h, x + w + (q / Math.sqrt(2)), y + h + (q / Math.sqrt(2)))
#         return self
#     },

#     ''' Рисует залитую окружность
#      * @param  {number} x - X центра
#      * @param  {number} y - Y центра
#      * @param  {number} radius - радиус
#      * @param  {number} startAngle=(15*PI/7) - Угол начала
#      * @param  {number} endAngle=(13*PI/2) - Угол конца
#      * @param  {bool} counterClockwise=False - По часовой стрелке?
#      * @returns {self}
#     '''
#     drawArc(x, y, radius,
#         startAngle,// = (15 * Math.PI / 7),
#         endAngle,// = (13 * Math.PI / 2),
#         counterClockwise = False) {

#         if (!startAngle) {
#             self.gfx.ellipse(x, y, radius, radius, self.Draw.color.getNumber())
#         } else {
#             self.gfx.pie(x, y, radius, self.deg(startAngle), self.deg(endAngle), self.Draw.color.getNumber())
#         }
#         return self
#     },

#     ''' Рисует залитую окружность
#      * @param  {number} x - X центра
#      * @param  {number} y - Y центра
#      * @param  {number} radius - радиус
#      * @param  {number} startAngle=(15*PI/7) - Угол начала
#      * @param  {number} endAngle=(13*PI/2) - Угол конца
#      * @param  {bool} counterClockwise=False - По часовой стрелке?
#      * @returns {self}
#     '''
#     fillArc(x, y, radius,
#         startAngle, // = (15 * Math.PI / 7),
#         endAngle = (13 * Math.PI / 2),
#         counterClockwise = False) {

#         if (!startAngle) {
#             self.gfx.ellipseFilled(x, y, radius, radius, self.Draw.color.getNumber())
#         } else {
#             self.gfx.pieFilled(x, y, radius, self.deg(startAngle), self.deg(endAngle), self.Draw.color.getNumber())
#         }
#         return self
#     },

#     ''' Рисует залитый четырехугольник по четырем точкам
#      * @param  {number} x1 - X 1 точки
#      * @param  {number} y1 - Y 1 точки
#      * @param  {number} x2 - X 2 точки
#      * @param  {number} y2 - Y 2 точки
#      * @param  {number} x3 - X 3 точки
#      * @param  {number} y3 - Y 3 точки
#      * @param  {number} x4 - X 4 точки
#      * @param  {number} y4 - Y 4 точки
#      * @returns {self}
#     '''
#     fillRect4(x1, y1, x2, y2, x3, y3, x4, y4) {
#         // self.ctx.beginPath()
#         // self.ctx.moveTo(x1, y1)
#         // self.ctx.lineTo(x2, y2)
#         // self.ctx.lineTo(x3, y3)
#         // self.ctx.lineTo(x4, y4)
#         // self.ctx.lineTo(x1, y1)
#         // self.ctx.closePath()
#         // self.ctx.fill(); //TODO:

#         return self
#     },

#     ''' Рисует четырехугольник по четырем точкам
#      * @param  {number} x1 - X 1 точки
#      * @param  {number} y1 - Y 1 точки
#      * @param  {number} x2 - X 2 точки
#      * @param  {number} y2 - Y 2 точки
#      * @param  {number} x3 - X 3 точки
#      * @param  {number} y3 - Y 3 точки
#      * @param  {number} x4 - X 4 точки
#      * @param  {number} y4 - Y 4 точки
#      * @returns {self}
#     '''
#     drawRect4(x1, y1, x2, y2, x3, y3, x4, y4) {
#         self.drawLine(x1, y1, x2, y2)
#         self.drawLine(x2, y2, x3, y3)
#         self.drawLine(x3, y3, x4, y4)
#         self.drawLine(x4, y4, x1, y1)

#         return self
#     },

#     ''' Рисует залитый триугольник по трем точкам
#      * @param  {number} x1 - X 1 точки
#      * @param  {number} y1 - Y 1 точки
#      * @param  {number} x2 - X 2 точки
#      * @param  {number} y2 - Y 2 точки
#      * @param  {number} x3 - X 3 точки
#      * @param  {number} y3 - Y 3 точки
#      * @returns {self}
#     '''
#     fillTriangle(x1, y1, x2, y2, x3, y3) {
#         /* self.ctx.beginPath()
#         self.ctx.moveTo(x1, y1)
#         self.ctx.lineTo(x2, y2)
#         self.ctx.lineTo(x3, y3)
#         self.ctx.lineTo(x1, y1)
#         self.ctx.closePath()
#         self.ctx.fill();'''

#         return self
#     },

#     ''' Рисует n-угольник по точкам
#      * @param  {array} array - Двумерный массив точек ([[x,y],[x1,y1],...])
#      * @returns {self}
#     '''
#     drawNangle(array) {
#         if (!(array && array.length)) {
#             console.warn('Аргументом оператора drawNangle должен быть двумерный массив!')
#             return self
#         }

#         self.ctx.beginPath()
#         for (let i = 0; i < array.length; i++) {
#             if (i == 0) self.ctx.moveTo(array[i][0], array[i][1])
#             else self.ctx.lineTo(array[i][0], array[i][1])
#         }
#         self.ctx.lineTo(array[0][0], array[0][0])
#         self.ctx.closePath()
#         self.ctx.stroke()
#         return self
#     },

#     ''' Рисует залитый n-угольник по точкам
#      * @param  {array} array - Двумерный массив точек ([[x,y],[x1,y1],...])
#      * @returns {self}
#     '''
#     fillNangle(array) {
#         if (!(array && array.length)) {
#             console.warn('Аргументом оператора fillNangle должен быть двумерный массив!')
#             return self
#         }

#         self.ctx.beginPath()
#         for (let i = 0; i < array.length; i++) {
#             if (i == 0) self.ctx.moveTo(array[i][0], array[i][1])
#             else self.ctx.lineTo(array[i][0], array[i][1])
#         }
#         self.ctx.lineTo(array[0][0], array[0][0])
#         self.ctx.closePath()
#         self.ctx.fill()
#         return self
#     },

#     ''' Рисует триугольник по трем точкам
#      * @param  {number} x1 - X 1 точки
#      * @param  {number} y1 - Y 1 точки
#      * @param  {number} x2 - X 2 точки
#      * @param  {number} y2 - Y 2 точки
#      * @param  {number} x3 - X 3 точки
#      * @param  {number} y3 - Y 3 точки
#      * @returns {self}
#     '''
#     drawTriangle(x1, y1, x2, y2, x3, y3) {
#         self.drawLine(x1, y1, x2, y2)
#         self.drawLine(x2, y2, x3, y3)
#         self.drawLine(x3, y3, x1, y1)

#         return self
#     },

#     '''
#      * @param  {string} text - Текст для отображения
#      * @param  {number} x - X
#      * @param  {number} y - Y
#      * @returns {self}
#     '''
#     drawString(text, x, y) {
#         /* self.ctx.fillText(text, x, y);'''
#         return self
#     },

#     ''' В некоторых реализациях JsMB используется двойная буфферизация
#      * repaint производит отрисовку на экран ранее произведенных действий
#      * В стандартной реализации ничего не делает
#      * @returns {self}
#     '''
#     repaint() {
#         self.ctx.present()
#         return self
#     },

#     ''' Задать размер шрифта
#      * @param  {number} size - Размер
#      * @returns {self}
#     '''
#     setFontSize(size) {
#         /* self.ctx.font = size + 'px ' + self.Font.family
#         self.Font.size = size;'''
#         return self
#     },

#     ''' Задать шрифт
#      * @param  {string} family - Шрифт
#      * @returns {self}
#     '''
#     setFont(family) {
#         /* self.ctx.font = self.Font.size + 'px ' + family
#         self.Font.family = family;'''
#         return self
#     },

#     ''' Создает линейный градиент
#      * @param  {number} x - X координата левого верхнего угла
#      * @param  {number} y - Y координата левого верхнего угла
#      * @param  {number} x1 - X координата правого нижнего угла
#      * @param  {number} y1 - Y координата правого нижнего угла
#      * @returns {self}
#     '''
#     makeLinearGradient(x, y, x1, y1) {
#         /* return self.ctx.createLinearGradient(x, y, x1, y1);'''
#         return null
#     },

#     ''' Создает радиальный (круговой) градиент
#      * @param  {number} x - X координата левого верхнего угла
#      * @param  {number} y - Y координата левого верхнего угла
#      * @param  {number} r - Радиус внутреннего круга
#      * @param  {number} x1 - X координата правого нижнего угла
#      * @param  {number} y1 - Y координата правого нижнего угла
#      * @param  {number} r1 - Радиус внешнего круга
#      * @returns {self}
#     '''
#     makeRadialGradient(x, y, r, x1, y1, r1) {
#         /* return self.ctx.createRadialGradient(x, y, r, x1, y1, r1);'''
#         return null
#     },

#     ''' Задать цвет градиенту
#      * @param  {gradient} g - Градиент
#      * @param  {number} pos - Позиция (0 - 1)
#      * @param  {string} color - Цвет в CSS формате
#      * @returns {self}
#     '''
#     setGradientColor(g, pos, color) {
#         // g.addColorStop(pos, color)
#         return self
#     },

#     // Конвертеры

#     ''' Цвет в rgb
#      * @param  {number} red=0 - Значение красного цвета (0 - 255)
#      * @param  {number} green=0 - Значение зеленого цвета (0 - 255)
#      * @param  {number} blue=0 - Значение синего цвета (0 - 255)
#      * @returns {string} "rgb(red, green, blue)"
#     '''
#     rgb(red = 0, green = 0, blue = 0) {
#         return [255, red, green, blue]
#     },

#     ''' Цвет в rgb
#      * @param  {number} red=0 - Значение красного цвета (0 - 255)
#      * @param  {number} green=0 - Значение зеленого цвета (0 - 255)
#      * @param  {number} blue=0 - Значение синего цвета (0 - 255)
#      * @param  {number} alpha=0 - Прозрачность (0 - 1)
#      * @returns {string} "rgba(red, green, blue, alpha)"
#     '''
#     rgba(red = 0, green = 0, blue = 0, alpha = 0) {
#         return [red, green, blue, alpha]
#     },

#     // Гели/спрайты

#     ''' Загрузить гель в память
#      * @param  {string} file - Файл (./,http,...)
#      * @param  {string} name - Имя геля
#      * @returns {self}
#     '''
#     gelLoad(file, name) {
#         self.Gel[name] = new Image()
#         self.Gel[name].src = file
#         return self
#     },

#     ''' [НЕ РЕАЛИЗОВАНО]
#      * Переводит гель в спрайт
#      * @param  {string} sprite - Имя спрайта
#      * @param  {string} gel - Имя геля
#      * @returns {self}
#     '''
#     spriteGel(/* sprite, gel''') {
#         console.warn('Внимание! Оператор spriteGel не работает!')
#         return self
#     },

#     ''' Рисует гель по указанным координатам
#      * @param  {string} name - Имя геля
#      * @param  {number} x - X координата левого верхнего угла
#      * @param  {number} y - Y координата левого верхнего угла
#      * @returns {self}
#     '''
#     drawGel(name, x, y) {
#         if (self.Gel[name].resize == True) {
#             self.ctx.drawImage(self.Gel[name], x, y, self.Gel[name].w, self.Gel[name].h)
#         } else {
#             self.ctx.drawImage(self.Gel[name], x, y)
#         }
#         return self
#     },

#     ''' [НЕ РЕАЛИЗОВАНО]
#      * Рисует спрайт по указанным координатам
#      * @param  {string} name - Имя спрайта
#      * @param  {number} x - X координата левого верхнего угла
#      * @param  {number} y - Y координата левого верхнего угла
#      * @returns {self}
#     '''
#     drawSprite(/* name, x, y''') {
#         console.warn('Внимание! Оператор drawSprite не работает!')
#         return self
#     },

#     ''' Задать размеры гелю (деформация)
#      * @param  {string} name - Название геля
#      * @param  {number} w - Ширина
#      * @param  {number} h - Высота
#      * @returns {self}
#     '''
#     gelSize(name, w, h) {
#         self.Gel[name].resize = True
#         self.Gel[name].w = w
#         self.Gel[name].h = h
#         return self
#     },

#     ''' Рисует фрагмент геля
#      * @param  {string} name - Имя геля
#      * @param  {number} fx - Координаты левого верхнего угла области
#      * @param  {number} fy - Координаты левого верхнего угла области
#      * @param  {number} fw - Ширина области
#      * @param  {number} fh - Высота области
#      * @param  {number} x - Координаты левого верхнего угла для рисования
#      * @param  {number} y - Координаты левого верхнего угла для рисования
#      * @param  {number} w=fw - ширина для рисования
#      * @param  {number} h=fh - высота для рисования
#      * @returns {self}
#     '''
#     drawGelFragment(name, fx, fy, fw, fh, x, y, w = fw, h = fh) { // TODO: Проверить
#         // self.ctx.drawImage(self.Gel[name], fx, fy, fw, fh, x, y, w, h)
#         return self
#     },

#     ''' Создает текстуру из геля
#      * @param  {string} gelname - Имя геля
#      * @param  {string} repeat='repeat' - Повторение (repeat/no-repeat)
#      * @returns {self}
#     '''
#     makeTexture(gelname, repeat = 'repeat') { // repeat/no-repeat
#         return self.ctx.createPattern(self.Gel[gelname], repeat)
#     },


#     // Ввод

#     ''' Окно ввода данных
#      * @param  {string} text - Текст заголовка окна
#      * @param  {string} [def] - Текст по умолчанию
#      * @returns {self}
#     '''
#     input(text, def) {
#         const tmp = prompt(text, def); // eslint-disable-line
#         return Number(tmp) || tmp
#     },


#     // Вывод

#     ''' Вывести текст на экран
#      * @returns {self}
#     '''
#     println(...text) {
#         const p = document.getElementById('p')

#         p.style = 'position:fixed;top:0px;left:0px;width:100%;height:100%;-webkit-user-select:none;    pointer-events: none;'
#         p.innerHTML += text + '<br/>'
#         return self
#     },

#     // Звук

#     ''' Играть звук
#      * @param  {string} file - Файл звука
#      * @param  {bool} loop - Зациклить?
#      * @param  {string} channel=0 - Канал
#      * @returns {self}
#     '''
#     playSound(file, loop = False, channel = 0) {
#         if (!self.Player[0]) {
#             console.warn('На вашей платформе не поддерживается воспроизведение звука!')
#             return self
#         }
#         if (self.Player[channel] === undefined) {
#             const p = document.createElement('audio')

#             p.id = 'player' + channel
#             document.getElementById('audio').appendChild(p)
#             self.Player[channel] = document.getElementById('player' + channel)
#         }
#         self.Player[channel].setAttribute('src', file)

#         self.Player[channel].setAttribute('loop', Number(loop))

#         self.Player[channel].play()
#         return self
#     },

#     ''' Приостановить воспроизведение звука на канале
#      * @param  {number} channel=-1 - Канал (-1 для остановки на всех каналах)
#      * @returns {self}
#     '''
#     pauseSound(channel = -1) {
#         if (!self.Player[0]) return self
#         if (channel == -1) {
#             for (const ch of self.Player) {
#                 ch.pause()
#             }
#             return self
#         }
#         if (self.Player[channel] === undefined) {
#             self.debug('На данном канале нет плеера')
#             return False
#         }
#         self.Player[channel].pause()
#         return self
#     },

#     // Matheматика

#     ''' Возвращает квадратный корень из числа
#      * @param  {number} number - Число
#      * @returns {number}
#     '''
#     'sqrt': number => Math.sqrt(number),

#     ''' Возвращает случайное число
#      * @param  {number} min - От
#      * @param  {number} max - До
#      * @returns {number}
#     '''
#     'random': (min, max) => Math.floor(Math.random() * max) + min,

#     ''' Возвращает синус угла
#      * @param  {number} angle - Угол в радианах
#      * @returns {number}
#     '''
#     'sin': angle => Math.sin(angle),

#     ''' Возвращает косинус угла
#      * @param  {number} angle - Угол в радианах
#      * @returns {number}
#     '''
#     'cos': angle => Math.cos(angle),

#     ''' Возвращает тангенс угла
#      * @param  {number} angle - Угол в радианах
#      * @returns {number}
#     '''
#     'tan': angle => Math.tan(angle),

#     ''' Возвращает котангенс угла
#      * @param  {number} angle - Угол в радианах
#      * @returns {number}
#     '''
#     'ctg': angle => 1 / Math.tan(angle),

#     ''' Возвращает арксинус угла (в радианах)
#      * @param  {number} number - Угол в радианах
#      * @returns {number}
#     '''
#     'asin': number => Math.asin(number),

#     ''' Возвращает арккосинус угла (в радианах)
#      * @param  {number} number - Угол в радианах
#      * @returns {number}
#     '''
#     'acos': number => Math.acos(number),

#     ''' Возвращает арктангенс угла (в радианах)
#      * @param  {number} number - Угол в радианах
#      * @returns {number}
#     '''
#     'atan': number => Math.atan(number),

#     ''' Возвращает остаток от деления 2-х чисел
#      * @param  {number} x - Делимое
#      * @param  {number} y - Делитель
#      * @returns {number}
#     '''
#     'mod': (x, y) => x % y,

#     ''' Возвращает модуль числа
#      * @param  {number} number - Число
#      * @returns {number}
#     '''
#     'abs': number => Math.abs(number),

#     ''' Возводит число в степень
#      * @param  {number} number - Число
#      * @param  {number} power - Степень
#      * @returns {number}
#     '''
#     'pow': (number, power) => Math.pow(number, power),

#     ''' Возвращает натуральный логарифм от числа
#      * @param  {number} number - Число
#      * @returns {number}
#     '''
#     'ln': number => Math.log(number),

#     ''' Возвращает число e в степени
#      * @param  {number} power - Степень
#      * @returns {number}
#     '''
#     'exp': power => Math.exp(power),

#     ''' Возвращает ограниченное значение переменной
#      * @param  {number} variable - Начальное значение
#      * @param  {number} min - Минимум (нижняя граница)
#      * @param  {number} max - Максимум (верхняя граница)
#      * @returns {number}
#     '''
#     limit(variable, min, max) {
#         return variable <= min ? min : max
#     },

#     ''' Возвращает минимальное значение из аргументов
#      * @returns {number}
#     '''
#     'min': (...a) => Math.min(...a),

#     ''' Возвращает максимальное значение из аргументов
#      * @returns {number}
#     '''
#     'max': (...a) => Math.max(...a),

#     ''' Переводит градусы в радианы
#      * @param  {number} deg - Значение в градусах
#      * @returns {number} Радианы
#     '''
#     rad(deg) {
#         if (deg === 90) return self.PI / 2
#         if (deg === 270) return 3 * self.PI / 2
#         return deg * self.DEG2RAD
#     },

#     ''' Переводит радианы в градусы
#      * @param  {number} rad - Значение в радианах
#      * @returns {number} Градусы
#     '''
#     deg(rad) {
#         return rad * self.RAD2DEG
#     },

#     // Строковые функции


#     ''' Возвращает длину строки/массива
#      * @param  {string} str - Строка/массив
#      * @returns {number}
#     '''
#     'len': str => str.length,

#     ''' Переводит число/значение в строку
#      * @param  {*} num - Число или другое значение
#      * @returns {string}
#     '''
#     'str': num => String(num),

#     ''' Переводит строку в число (или возвращает NaN, если это невозможно)
#      * @param  {string} str - Строка с числом
#      * @returns {number}
#     '''
#     'val': str => Number(str),

#     ''' Переводит строку в число (или возвращает NaN, если это невозможно)
#      * Лучше использовать val
#      * @param  {string} str - Строка с числом
#      * @param  {number} [system=10] - Система исчисления
#      * @returns {number} Int
#     '''
#     int(str, system = 10) {
#         return parseInt(str, system)
#     },

#     ''' Переводит строку в число с плавающей точкой (или возвращает NaN, если это невозможно)
#      * @param  {string} str - Строка с числом
#      * @returns {number} Float
#     '''
#     'float': str => parseFloat(str),

#     ''' Приводит все символы строки в ВЕРХНИЙ РЕГИСТР
#      * @param  {string} str - Строка
#      * @returns {string}
#     '''
#     'upper': str => str.toUpperCase(),

#     ''' Приводит все символы строки в нижний регистр
#      * @param  {string} str - Строка
#      * @returns {string}
#     '''
#     'lower': str => str.toLowerCase(),

#     ''' Возвращает часть строки
#      * @param  {string} str - Строка
#      * @param  {number} pos - Начало выделения
#      * @param  {number} len - Длина выделения
#      * @returns {string}
#     '''
#     'mid': (str, pos, len) => str.substr(pos, len),

#     ''' Возвращает символ по его коду. Можно передать несколько кодов
#      * @param  {number} code - Код(ы) символа
#      * @returns {string}
#     '''
#     'chr': (...codes) => String.fromCharCode(...codes), // code to string

#     ''' Возвращает код символа
#      * @param  {string} str - Строка
#      * @param  {number} [pos=0] - Позиция символа в строке
#      * @returns {number}
#     '''
#     'asc': (str, pos = 0) => str.charCodeAt(pos), // string to code

#     ''' Разбивает строку и возвращает массив частей
#      * @param  {string} str - Строка
#      * @param  {string} char - Символ/регулярное выражение, по которому разбивать
#      * @returns {array}
#     '''
#     'split': (str, char) => str.split(char),

#     ''' Переводит массив в строку, разделяя элементы разделителем
#      * @param  {array} array - массив
#      * @param  {string} [separator=' '] - разделитель
#      * @returns {string}
#     '''
#     'join': (array, separator = ' ') => array.join(separator),

#     ''' Возвращает строку с замененной частью
#      * @param  {string} str - Строка
#      * @param  {string} reg - Строка/регулярное выражение для замены
#      * @param  {string} to - На что менять
#      * @param  {bool} [all=False] - Заменять все включения
#      * @returns {string}
#     '''
#     replace(str, reg, to, all = False) {
#         if (all) return str.replace(new RegExp(reg, 'g'))
#         return str.replace(reg, to)
#     },

#     // Работа с локальными данными

#     ''' Сохранить данные в хранилище
#      * @param  {string} name - Название ячейки
#      * @param  {*} _data - Данные
#      * @returns {self}
#     '''
#     localSaveData(name, _data) {
#         const data = typeof (_data) == 'object' ? self.toJSON(_data) : _data

#         window.localStorage.setItem(name, data)
#         return self
#     },

#     ''' Получить данные из хранилища
#      * @param  {string} name - Название ячейки
#      * @returns {object}
#     '''
#     localReadData(name) {
#         /* try {
#             return self.parseJSON(window.localStorage.getItem(name))
#         } catch (e) {
#             return window.localStorage.getItem(name)
#         }'''
#     },

#     ''' Возвращает объект из JSON строки
#      * @param  {string} json - JSON строка
#      * @returns {object}
#     '''
#     'parseJSON': (json) => {
#         try {
#             return JSON.parse(json)
#         } catch (e) {
#             return null
#         }
#     },

#     ''' Возвращает JSON строку из объекта
#      * @param  {object} object - Объект
#      * @param  {function} [f=null] - Дополнительный обработчик
#      * @param  {number} [s=4] - Отступ
#      * @returns {string}
#     '''
#     'toJSON': (object, f = null, s = 4) => JSON.stringify(object, f, s),

#     ''' Возвращает PSON строку из объекта (с функциями)
#      * @param  {object} object - Объект
#      * @param  {number} [s=4] - Отступ
#      * @returns {string}
#     '''
#     'toPSON': (object, s = 4) => JSON.stringify(object, (a, b) => typeof b === 'function' ? String(b) : b, s), // eslint-disable-line

#     // Работа с модулями

#     ''' Подключает модуль/файл
#      * @param  {string} file - Имя/адрес файла
#      * @returns {self}
#     '''
#     include(file) {
#         //TODO:FIXME:
#         /* const e = document.createElement('script')

#         e.src = file
#         e.type = 'text/javascript'
#         document.getElementById('modules').appendChild(e);'''
#         return self
#     },

#     getModuleName(ID) {
#         console.warn('self function is deprecated!')
#         return ID.name
#     },

#     getModuleAuthor(ID) {
#         console.warn('self function is deprecated!')
#         return ID.author
#     },

#     getModuleDescription(ID) {
#         console.warn('self function is deprecated!')
#         return ID.description
#     },

#     getModuleUrl(ID) {
#         console.warn('self function is deprecated!')
#         return ID.url
#     },

#     getModuleVersion(ID) {
#         console.warn('self function is deprecated!')
#         return ID.version
#     },

#     // Получение значений

#     ''' Возвращает ширину экрана
#      * @returns {number}
#     '''
#     screenWidth() {
#         return self.c.size.w
#     },

#     ''' Возвращает высоту экрана
#      * @returns {number}
#     '''
#     screenHeight() {
#         return self.c.size.h
#     },

#     ''' Возвращает X координату мыши в данный момент
#      * @returns {number}
#     '''
#     getMouseX() {
#         return self.Mouse.x
#     },

#     ''' Возвращает Y координату мыши в данный момент
#      * @returns {number}
#     '''
#     getMouseY() {
#         return self.Mouse.y
#     },

#     ''' Возвращает количество кликов с момента запуска программы
#      * @returns {number}
#     '''
#     getLeftClicksCount() {
#         return self.Mouse.lcount
#     },

#     ''' Возвращает количество правых кликов с момента запуска программы
#      * @returns {number}
#     '''
#     getRightClicksCount() {
#         return self.Mouse.rcount
#     },


#     // Техническое

#     ''' Логирование
#      * @param  {*} - Данные
#      * @returns {self}
#     '''
#     log(...text) {
#         console.log(...text)
#         return self
#     },

#     ''' Вывести сообщение для отладки
#      * @param  {string} text - Сообщение
#      * @param  {string} [style] - Оформление сообщения (CSS)
#      * @returns {self}
#     '''
#     debug(text) {
#         if (Config.Debug_Mode) {
#             console.log(text)
#         }
#         return self
#     },

#     ''' Закрыть программу
#      * @returns {self}
#     '''
#     exit() {
#         process.exit(0)
#         return self
#     },

#     _Color: class {
#         constructor(color) {
#             {
#                 self.getRgbArray = self.getRgbArray.bind(self)
#                 self.getArgbArray = self.getArgbArray.bind(self)
#                 self.getHex = self.getHex.bind(self)
#                 self.getNumber = self.getNumber.bind(self)
#                 self.getObject = self.getObject.bind(self)
#             }
#             self._color = { a: 0, r: 0, g: 0, b: 0 }
#             if (typeof color === 'number') {
#                 self._color = {
#                     a: (color >> 24) & 0xFF,
#                     r: (color >> 16) & 0xFF,
#                     g: (color >> 8) & 0xFF,
#                     b: (color >> 0) & 0xFF
#                 }
#             }
#             else if (typeof color === 'object') {
#                 if(color instanceof JsMB._Color) {
#                     self._color = color._color
#                 }
#                 else if (color instanceof Array) {
#                     if (color.length === 4) {
#                         if (color[3] > 0 && color[3] <= 1) {
#                             //Css RGBA format
#                             self._color = {
#                                 a: (color[3] * 1000) & 0xFF,
#                                 r: color[0],
#                                 g: color[1],
#                                 b: color[2]
#                             }
#                         }
#                         else {
#                             //[TEMP] SDL ARGB format
#                             self._color = {
#                                 a: color[0],
#                                 r: color[1],
#                                 g: color[2],
#                                 b: color[3]
#                             }
#                         }
#                     }
#                     else {
#                         //TODO: RGB
#                         JsMB.debug(`[COLOR] Неизвестный формат массива цвета!`)
#                         self._color = { a: 0, r: color[0] || 0, g: color[1] || 0, b: color[2] || 0 }
#                     }
#                 }

#                 else if (color.r + 1 && color.g + 1 && color.b + 1 && color.a + 1) {
#                     self._color = color
#                 }

#                 else {
#                     JsMB.debug(`[COLOR] Неизвестный формат цвета!`)
#                     self._color = { a: 0, r: 0, g: 0, b: 0 }
#                 }
#             }
#         }

#         getRgbArray() {
#             const c = self._color
#             return [c.r, c.g, c.b]
#         }

#         getArgbArray() {
#             const c = self._color
#             return [c.a, c.r, c.g, c.b]
#         }

#         getHex() {}

#         getNumber() {
#             //FIXME: Можно проще
#             const c = self._color
#             let a = c.a.toString(16)
#                 a = a.length === 1 ? '0'+a : a
#             let r = c.r.toString(16)
#                 r = r.length === 1 ? '0' + r : r
#             let g = c.g.toString(16)
#                 g = g.length === 1 ? '0' + g : g
#             let b = c.b.toString(16)
#                 b = b.length === 1 ? '0' + b : b
#             return Number(`0x{a}{r}{g}{b}`)
#         }

#         getObject() {
#             return self._color
#         }
#     },

#     // Обработчики событий TODO:
#     _eventListeners() {
#         // window.onClick =
#         //     window.onMouseDown = window.onMouseMove = window.onMouseUp = window.onKeyDown = window.onKeyPress = window.onKeyUp = window.onRightClick = window.Loop = () => {}
#         self.c.addEventListener('mousemove', (event) => {
#             self.Mouse.x = event.offsetX
#             self.Mouse.y = event.offsetY
#             if (typeof onMouseMove === 'function')
#                 onMouseMove(event.offsetX, event.offsetY, event)
#         }, False)
#         self.c.addEventListener('click', (event) => {
#             self.Mouse.lcount++
#             if (typeof onClick === 'function')
#                 onClick(event.offsetX, event.offsetY, event)
#         }, False)
#         self.c.addEventListener('mousedown', (event) => {
#             if (typeof onMouseDown === 'function')
#                 onMouseDown(event.offsetX, event.offsetY, event)
#         }, False)
#         self.c.addEventListener('mouseup', (event) => {
#             if (typeof onMouseUp === 'function')
#                 onMouseUp(event.offsetX, event.offsetY, event)
#         }, False)
#         self.c.addEventListener('contextmenu', (event) => {
#             self.Mouse.rcount++
#             if (typeof onRightClick === 'function')
#                 onRightClick(event.offsetX, event.offsetY, event)
#         }, False)
#         window.addEventListener('keypress', (event) => {
#             if (typeof onKeyPress === 'function')
#                 onKeyPress(event.keyCode, event)
#         }, False)

#         window.addEventListener('keydown', (event) => {
#             if (typeof onKeyDown === 'function')
#                 onKeyDown(event.keyCode, event)
#         }, False)

#         window.addEventListener('keyup', (event) => {
#             if (typeof onKeyUp === 'function')
#                 onKeyUp(event.keyCode, event)
#         }, False)
#     }
# }
# // ======Прочее======//

# JsMB.__preinit()
# if (JsMB.JsMobileBasic.supports.browser && Config.mount_window) {
#     Object.assign(window, JsMB)
#     JsMB.__init()
# } else {
#     JsMB.__init()
# }

# if (typeof module === 'object') module.exports = JsMB

# JsMB.debug('// ======Инициализация завершена======//', 'background:black;color: #00ff00;')

# if (typeof window !== 'undefined') window.addEventListener('load', () => {
#     JsMB._eventListeners()
#     if (typeof Main === "function") Main(); //eslint-disable-line
#     else throw new Error('В файле Autorun.bas должен быть хук Main()!')
#     if (typeof Loop === 'function') {
#         if (!window.requestAnimationFrame) {
#             window.requestAnimationFrame = (window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame || window.oRequestAnimationFrame || function (fnc) {
#                 return window.setTimeout(fnc, 1000 / 60)
#             })
#         }

#         function Loop() { //eslint-disable-line
#             window.requestAnimationFrame(Loop)
#             Loop()
#         }
#         Loop()
#     }
# })

class Color():
    def __init__(self, color):
        self._color = { 'a': 0, 'r': 0, 'g': 0, 'b': 0 }

        if (type(color) == list or type(color) == tuple) and len(color) == 1: color = color[0]

        if type(color) == int:
            self._color = {
                'a': (color >> 24) & 0xFF,
                'r': (color >> 16) & 0xFF,
                'g': (color >> 8) & 0xFF,
                'b': (color >> 0) & 0xFF
            }
        elif type(color) == Color:
            self._color = color.getObject()
        elif type(color) == list or type(color) == tuple:
            if len(color) == 4:
                if color[3] > 0 and color[3] <= 1:
                    # Css RGBA format
                    self._color = {
                        'a': (color[3] * 1000) & 0xFF,
                        'r': color[0],
                        'g': color[1],
                        'b': color[2]
                    }
                else:
                    # [TEMP] SDL ARGB format
                    self._color = {
                        'a': color[0],
                        'r': color[1],
                        'g': color[2],
                        'b': color[3]
                    }
            else:
                # TODO: RGB
                JsMB.Debug('[COLOR] Неизвестный формат массива цвета!', color)
                self._color = { 'a': 0, 'r': color[0] or 0, 'g': color[1] or 0, 'b': color[2] or 0 }

        elif type(color) == dict and ('r' in color) and ('g' in color) and ('b' in color):
            if 'a' in color:
                self._color = {
                    'a': color['a'],
                    'r': color['r'],
                    'g': color['g'],
                    'b': color['b']
                }
            else:
                self._color = {
                    'a': 255,
                    'r': color['r'],
                    'g': color['g'],
                    'b': color['b']
                }
        else:
            JsMB.Debug('[COLOR] Неизвестный формат цвета!', color)
            self._color = { 'a': 0, 'r': 0, 'g': 0, 'b': 0 }

    def getRgbArray(self):
        c = self._color

        return (c['r'], c['g'], c['b'])

    def getRgbaArray(self):
        return (*self.getRgbArray(), self._color['a'])

    def getArgbArray(self):
        c = self._color
        
        return (c['a'], c['r'], c['g'], c['b'])

    def getHex(self):
        c = self._color

        a = hex(c['a'])[2:]
        if len(a) == 1:
            a = '0' + a
        r = hex(c['r'])[2:]
        if len(r) == 1:
            r = '0' + r
        g = hex(c['g'])[2:]
        if len(g) == 1:
            g = '0' + g
        b = hex(c['b'])[2:]
        if len(b) == 1:
            b = '0' + b

        return '0x' + a + r + g + b

    def getRGBHex(self):
        c = self._color

        r = hex(c['r'])[2:]
        if len(r) == 1:
            r = '0' + r
        g = hex(c['g'])[2:]
        if len(g) == 1:
            g = '0' + g
        b = hex(c['b'])[2:]
        if len(b) == 1:
            b = '0' + b

        return '0x' + r + g + b

    def getNumber(self):
        return int(self.getHex(), base=16)

    def getObject(self):
        return self._color