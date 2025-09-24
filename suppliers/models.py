from django.core.exceptions import ValidationError
from django.db import models


class Node(models.Model):
    """
    Узел сети поставок.

    Parameters
    ----------
    name : str
        Наименование узла.
    email : str
        Адрес электронной почты.
    country : str
        Страна расположения.
    city : str
        Город.
    street : str
        Улица.
    house_number : str
        Номер дома.
    supplier : Node, optional
        Поставщик оборудования (родительский узел). Может быть ``None``.
    debt : Decimal, default=0
        Сумма задолженности узла.
    created_at : datetime
        Дата и время создания записи (устанавливается автоматически).

    Properties
    ----------
    level : int
        Уровень узла в иерархии сети. Завод всегда имеет уровень 0.

    Methods
    -------
    clean()
        Проверяет ограничения узла:
        - уровень не выше 2,
        - отсутствуют циклы в цепочке поставщиков.
    """

    class Meta:
        indexes = [models.Index(fields=['country']), models.Index(fields=['city']), ]
        ordering = ['name']

        verbose_name = 'Узел сети поставок'
        verbose_name_plural = 'Узлы сети поставок'

    name = models.CharField(max_length=60, verbose_name='Наименование')

    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=60)
    country = models.CharField(verbose_name='Страна', max_length=50)
    city = models.CharField(verbose_name='Город', max_length=50)
    street = models.CharField(verbose_name='Улица', max_length=80)
    house_number = models.CharField(verbose_name='Номер дома', max_length=10)

    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def level(self):
        """
        Вычисляет уровень узла в иерархии сети.

        Returns
        -------
        int
            Уровень узла (0 — завод, 1 — первый уровень, 2 — второй уровень).
        """
        lvl = 0
        supplier = self.supplier
        while supplier:
            lvl += 1
            supplier = supplier.supplier
        return lvl

    def clean(self):
        """
        Проверяет корректность узла перед сохранением.

        Raises
        ------
        ValidationError
            Если уровень узла превышает 2 или есть циклическая ссылка на поставщика.
        """
        if self.level > 2:
            raise ValidationError('Узел не может быть глубже 2-го уровня')

        supplier = self.supplier
        while supplier:
            if supplier == self:
                raise ValidationError('Недопустима циклическая ссылка на поставщика')
            supplier = supplier.supplier


class Product(models.Model):
    """
    Продукт, закреплённый за конкретным узлом сети.

    Parameters
    ----------
    name : str
        Наименование продукта.
    model : str
        Модель продукта.
    release_date : date
        Дата выхода продукта на рынок.
    owner : Node
        Узел-владелец продукта.
    """

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(verbose_name='Наименование', max_length=60)
    model = models.CharField(verbose_name='Модель', max_length=20)
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')
    owner = models.ForeignKey(Node, related_name='products', on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.name} от {self.owner.name}'
