## Курсовая работа на тему "Извлечение логической структуры из сканированных документов"

### Постановка задачи

Целью моей курсовой работы является разработка метода выделения логической структуры из документов в виде глав, подглав (и т. д.), элементов нумерованных и маркированных списков.
Необходимо классифицировать каждую строчку документа как заголовок, элемент списка или текст.

### Содержимое репозитория

* articles - статьи с существующими решениями похожих задач;

* different_docs - папка с документами, на которых ошибается классификатор;

* docs - документы для обучения классификатора;

* examples - примеры документов и черновой ноутбук для тренировки;

* latex - текущий текст курсовой работы в форматах .tex и .pdf;

* data.json - размеченные данные;

* feature_importances.xlsx - важность признаков при обучении классификатора;

* pipeline.ipynb - основной файл с кодом для извлечения признаков, обучения классификатора, анализа результатов;

* unite_json.ipynb - объединение отдельных размеченных json файлов для каждого документа в общий файл data.json.

Пример разметки документа:

![alt text](./latex/pics/example.png)