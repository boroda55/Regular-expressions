# Обработка с помощью Regular expressions
## Реализовано
###
- Перемещены Фамилии, Имена и Отчества людей в поля lastname, firstname и surname соответственно. В записной книжке изначально было Ф + ИО, ФИО и Ф+И+О. Подсказка: работал со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" ").
- Приведены все телефоны к формату +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999. Подсказка: использовал регулярки для обработки телефонов.
- Объединил все дублирующиеся записи о человеке в одну. Подсказка: группировал записи по ФИО.

### Добавлено логирование