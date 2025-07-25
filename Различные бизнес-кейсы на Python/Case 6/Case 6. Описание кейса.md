# Кейс 6. Автотестирование кода пользователей

Начнем, пожалуй, с самого интересного, и хоть и небольшого, но самого сложного кейса на наш взгляд.

Мы предлагаем вам написать автоматическую систему проверки кода, прямо как у нас на `itresume`! Конечно, повторить полную архитектуру, у нас наверное не хватит ни времени, ни навыков, но написать небольшую копию - вполне!

**Чего мы от вас ожидаем?**

Мы дадим вам два файла `.py` - эталонный код и код пользователя, а вам необходимо будет написать систему, которая проверит их на заданных тестовых случаях и вернет соответствующие результаты. Прямо как при решении задач у нас.

Думаем вы справитесь, тем более мы собрали для вас подсказки, которые точно помогут!

Первое, что пожалуй вызывает вопросы: А как мы будем запускать код пользователя и эталонный? А очень легко - всппоминайте **урок 9** о модулях и библиотеках. Мы обсуждали, что возможно задать свой модуль и свою функцию - `from my_module import my_function`.

И учитывая, что решения будут даны вам в `.py` файлах - вы можете воспользоваться модулем `importlib`, который используется для динамической загрузки модулей в Python. В данном случае, мы сможем импортировать два модуля: например `etalon` и `user`, содержащие эталонное и пользовательское решения соответственно.

**Как это сделать?**

Модуль `importlib` содержит метод `import_module` и использовать его можно так:

А дальше все еще проще, когда у нас есть два модуля для эталонного ответа и ответа студента, мы можем просто вызвать методы из этих модулей.

**Важно**: для корректной работы понадобится проверить, что за функции содержатся в кодах. Так как вызывать вы их будете следующим образом:

Ссылка на документацию по модулю `importlib`

[**importlib**](https://docs.python.org/3/library/importlib.html)

Теперь, когда мы немного разобрались с `importlib`, продолжим об автопроверке.

**Как корректно проверить код?**

Каждый код необходимо прогнать на тестовых случах, которые будут даны в шаблоне. Если код будет возвращать ошибку - эту ошибку необходимо записать в файл `output.txt` в следующем формате: `"Ошибка при выполнении кода пользователя: {}"`, где будет указана полученная ошибка. Причем, в таком случае, работа автопроверки должна остановиться.

Если же код не вызывает никаких ошибок, мы можем проверить все тестовые случаи. Если код проходит тестовый случай - то есть результат кода студента равен результату эталонного кода - запишите в файл `"Тест пройден"`. Например, наш код прошел 4 тестовых случая и не вызывал никаких ошибок, итоговый файл `output.txt`, содержащий результат будет выглядеть так:

Если же тестовый случай не пройден - как и на `itresume` надо вывести ожидаемый результат и результат пользователя. Например код тестировался 1 раз и не прошел тест, файл `output.txt` будет выглядеть так:

Для первой части кейса - это все, что вам нужно знать, поэтому продвигаемся дальше!

**Вторая часть**

Одна из важнейших частей автопроверки - предварительная проверка кода пользователя на наличие вредоносного кода. Теперь нам нужно к коду написанному в прошлой части добавить проверку на вредоносность.

Для этого мы предлагаем вам написать отдельную функцию `check_for_malicious_code`, которая будет принимать код и путь к файлу. Для реализации этой функции также предлагаем вам использовать модуль `ast`, который позволяет анализировать и деревья синтаксического разбора кода на Python. Звучит очень сложно, но давайте по шагам:

Что делает функция `check_for_malicious_code`:

- Функция принимает два аргумента: `code` и `output_file`. Аргумент `code` содержит код, который нужно проверить на наличие вредоносных элементов. Аргумент `output_file` содержит имя файла, в который будут записываться результаты проверки.
- Далее, функция использует модуль `ast` для анализа кода. Анализ происходит в два этапа:
- С помощью функции `ast.parse(code)` создается объект-дерево, которое представляет структуру синтаксического разбора кода.
- Затем, с помощью функции `ast.walk(tree)` происходит обход дерева и поиск запрещенных элементов.

В процессе обхода дерева, функция ищет **несколько типов запрещенных элементов**:

- Атрибуты с именами, перечисленными в списке `FORBIDDEN_NAMES`, к ним относятся `(exec)`. Если такой атрибут найден, то функция выбрасывает исключение `ValueError` и записывается сообщение: `Код содержит запрещенный атрибут: {имя}`.
- Если в коде вызывается `eval` без аргументов - вызовите исключение `ValueError` и запишите соответствующее сообщение в файл: `Код содержит вызов eval()`.
- Если при анализе кода возникает синтаксическая или ошибка, перехватите её и запишите в файл соответствующую ошибку `Код содержит синтаксическую ошибку: {тип ошибки}`.
- Если в коде обнаруживаются другие ошибки, запишите в файл `Код содержит вредоносные элементы: {}`.

Если в коде обнаруживаются запрещенные элементы или возникает синтаксическая ошибка, то функция **должна завершить** свою работу и вернуть соответствующую ошибку.

**Важно**: предварительно, если вызов функции `check_for_malicious_code` вызывает любую ошибку - в файл необходимо записать: `"Ошибка при проверке модуля user_malicious:"` и на следующей строке записать детали ошибок, описанные выше.

Если же все проверки пройдены успешно, то функция должна продолжить тестирование кода.

Давайте сразу к примерам. Например, код пользователя содержит некоторую синтаксическую ошибку. При вызове `check_for_malicious_code` в выходном файле мы получим:

**Третья часть**

Когда большая часть работы сделана - давайте добавим простую, но не менее важную проверку - на время выполнения кода. Если код студента содержит бесконечный цикл, нежелательно, чтобы наша программа работала так же бесконечно. Поэтому давайте ограничим время пятью секундами.

Для реализации этого мы предлагаем вам воспользоваться двумя модулями - `time` и `multiprocessing`.

Модуль `time` позволит нам подсчитать время выполнения, однако, если мы получим код с бесконечным циклом и прямо внутри нашей системы попробуем это подсчитать - наш код просто будет подсчитывать время бесконечно. Поэтому нам нужен второй модуль - `multiprocessing`, который позволит нам вынести выполнение функции в отдельный процесс и замерить его время. Это позволит нам и избежать блокировки основного потока и добавить логику превышения допустимого порога времени.

Давайте подробнее рассмотрим методы, которые вам могут понадобиться:

- Функция `time.time()` - возвращает количество секунд, прошедших с начала эпохи (обычно 1 января 1970 года). Эту функцию можно использовать для измерения времени выполнения кода.
- Класс `multiprocessing.Process` - позволяет запускать параллельные процессы. Он принимает на вход функцию, которую нужно выполнить в отдельном потоке, и набор аргументов этой функции. А именно, например `multiprocessing.Process(target=user_code)` создает объект класса `Process`, который может быть запущен в отдельном процессе. Аргумент `target` принимает функцию, которую нужно выполнить в отдельном процессе (в нашем случае функцию пользователя).
- `process.start()` запускает созданный объект процесса. Как только этот метод вызывается, Python создает новый процесс, в котором запускает код, переданный в аргументе `target`.
- `process.join(timeout=...)` ждет завершения процесса. Он блокирует основной поток исполнения программы до тех пор, пока не завершится процесс, на который указывает объект `process`. Аргумент `timeout` задает максимальное количество времени, которое `join()` будет ожидать завершения процесса. В данном случае, если процесс не завершился в течение 10 секунд, он будет прерван.

И вот теперь, наконец-то, приглашаем вас в [**Google Colab**](https://colab.research.google.com/drive/1Dw_H7TbCcx2pa7d8_iW3bB0EvxaGstWv?usp=sharing) - копируйте блокнот и попробуйте свои силы в этом непростом кейсе!
