# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actividad(models.Model):
    codactividad = models.AutoField(db_column='codActividad', primary_key=True)  # Field name made lowercase.
    nombreactividad = models.CharField(db_column='nombreActividad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Actividad'
        
    def __str__(self):
        return self.nombreactividad



class Antecedente(models.Model):
    codantecedente = models.AutoField(db_column='codAntecedente', primary_key=True)  # Field name made lowercase.
    nombreantecedente = models.CharField(db_column='nombreAntecedente')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Antecedente'

    def __str__(self):
        return self.nombreantecedente


class Antecedentevictima(models.Model):
    pk = models.CompositePrimaryKey('antecedente', 'victima')
    antecedente = models.ForeignKey(Antecedente, models.DO_NOTHING, db_column='antecedente')
    victima = models.ForeignKey('Victima', models.DO_NOTHING, db_column='victima')

    class Meta:
        managed = False
        db_table = 'AntecedenteVictima'


class Ccaa(models.Model):
    codccaa = models.AutoField(db_column='codCCAA', primary_key=True)  # Field name made lowercase.
    nombreccaa = models.CharField(db_column='nombreCCAA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CCAA'
    
    def __str__(self):
        return self.nombreccaa


class Causa(models.Model):
    codcausa = models.AutoField(db_column='codCausa', primary_key=True)  # Field name made lowercase.
    nombrecausa = models.CharField(db_column='nombreCausa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Causa'

    def __str__(self):
        return self.nombrecausa


class Causavictima(models.Model):
    pk = models.CompositePrimaryKey('causa', 'victima')
    causa = models.ForeignKey(Causa, models.DO_NOTHING, db_column='causa')
    victima = models.ForeignKey('Victima', models.DO_NOTHING, db_column='victima')

    class Meta:
        managed = False
        db_table = 'CausaVictima'


class Deteccion(models.Model):
    coddeteccion = models.AutoField(db_column='codDeteccion', primary_key=True)  # Field name made lowercase.
    nombredeteccion = models.CharField(db_column='nombreDeteccion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Deteccion'

    def __str__(self):
        return self.nombredeteccion


class Extraccion(models.Model):
    codextraccion = models.AutoField(db_column='codExtraccion', primary_key=True)  # Field name made lowercase.
    nombreextraccion = models.CharField(db_column='nombreExtraccion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Extraccion'

    def __str__(self):
        return self.nombreextraccion


class Factorriesgo(models.Model):
    codfactorriesgo = models.AutoField(db_column='codFactorRiesgo', primary_key=True)  # Field name made lowercase.
    nombrefactorriesgo = models.CharField(db_column='nombreFactorRiesgo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactorRiesgo'

    def __str__(self):
        return self.nombrefactorriesgo


class Factorriesgovictima(models.Model):
    pk = models.CompositePrimaryKey('factorriesgo', 'victima')
    factorriesgo = models.ForeignKey(Factorriesgo, models.DO_NOTHING, db_column='factorRiesgo')  # Field name made lowercase.
    victima = models.ForeignKey('Victima', models.DO_NOTHING, db_column='victima')

    class Meta:
        managed = False
        db_table = 'FactorRiesgoVictima'


class Incidente(models.Model):
    codincidente = models.AutoField(db_column='codIncidente', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    titular = models.CharField()
    latitud = models.TextField()
    longitud = models.TextField()
    enlace = models.CharField(blank=True, null=True)
    actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='actividad')
    deteccion = models.ForeignKey(Deteccion, models.DO_NOTHING, db_column='deteccion')
    intervencion = models.ForeignKey('Intervencion', models.DO_NOTHING, db_column='intervencion')
    localidad = models.ForeignKey('Localidad', models.DO_NOTHING, db_column='localidad')
    localizacion = models.ForeignKey('Localizacion', models.DO_NOTHING, db_column='localizacion')
    riesgo = models.ForeignKey('Riesgo', models.DO_NOTHING, db_column='riesgo')
    zona = models.ForeignKey('Zonavigilada', models.DO_NOTHING, db_column='zona')

    class Meta:
        managed = False
        db_table = 'Incidente'


class Intervencion(models.Model):
    codintervencion = models.AutoField(db_column='codIntervencion', primary_key=True)  # Field name made lowercase.
    nombreintervencion = models.CharField(db_column='nombreIntervencion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Intervencion'

    def __str__(self):
        return self.nombreintervencion


class Localidad(models.Model):
    codlocalidad = models.AutoField(db_column='codLocalidad', primary_key=True)  # Field name made lowercase.
    nombrelocalidad = models.CharField(db_column='nombreLocalidad')  # Field name made lowercase.
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='provincia')

    class Meta:
        managed = False
        db_table = 'Localidad'

    def __str__(self):
        return self.nombrelocalidad


class Localizacion(models.Model):
    codlocalizacion = models.AutoField(db_column='codLocalizacion', primary_key=True)  # Field name made lowercase.
    nombrelocalizacion = models.CharField(db_column='nombreLocalizacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Localizacion'

    def __str__(self):
        return self.nombrelocalizacion


class Materialrescate(models.Model):
    codmaterialrescate = models.AutoField(db_column='codMaterialRescate', primary_key=True)  # Field name made lowercase.
    nombrematerialrescate = models.CharField(db_column='nombreMaterialRescate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MaterialRescate'

    def __str__(self):
        return self.nombrematerialrescate


class Nacionalidad(models.Model):
    codnacionalidad = models.AutoField(db_column='codNacionalidad', primary_key=True)  # Field name made lowercase.
    nombrenacionalidad = models.CharField(db_column='nombreNacionalidad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Nacionalidad'

    def __str__(self):
        return self.nombrenacionalidad


class Origen(models.Model):
    codorigen = models.AutoField(db_column='codOrigen', primary_key=True)  # Field name made lowercase.
    nombreorigen = models.CharField(db_column='nombreOrigen')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Origen'

    def __str__(self):
        return self.nombreorigen


class Primerinterviniente(models.Model):
    codprimerinterviniente = models.AutoField(db_column='codPrimerInterviniente', primary_key=True)  # Field name made lowercase.
    nombreprimerinterviniente = models.CharField(db_column='nombrePrimerInterviniente')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PrimerInterviniente'

    def __str__(self):
        return self.nombreprimerinterviniente


class Pronostico(models.Model):
    codpronostico = models.AutoField(db_column='codPronostico', primary_key=True)  # Field name made lowercase.
    nombrepronostico = models.CharField(db_column='nombrePronostico')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pronostico'

    def __str__(self):
        return self.nombrepronostico


class Provincia(models.Model):
    codprovincia = models.AutoField(db_column='codProvincia', primary_key=True)  # Field name made lowercase.
    nombreprovincia = models.CharField(db_column='nombreProvincia')  # Field name made lowercase.
    codccaa = models.ForeignKey(Ccaa, models.DO_NOTHING, db_column='codCCAA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Provincia'

    def __str__(self):
        return self.nombreprovincia


class Reanimacion(models.Model):
    codreanimacion = models.AutoField(db_column='codReanimacion', primary_key=True)  # Field name made lowercase.
    nombrereanimacion = models.CharField(db_column='nombreReanimacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reanimacion'


class Riesgo(models.Model):
    codriesgo = models.AutoField(db_column='codRiesgo', primary_key=True)  # Field name made lowercase.
    nombreriesgo = models.CharField(db_column='nombreRiesgo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riesgo'

    def __str__(self):
        return self.nombreriesgo


class Tipoahogamiento(models.Model):
    codtipoahogamiento = models.AutoField(db_column='codTipoAhogamiento', primary_key=True)  # Field name made lowercase.
    nombretipoahogamiento = models.CharField(db_column='nombreTipoAhogamiento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoAhogamiento'

    def __str__(self):
        return self.nombretipoahogamiento


class Victima(models.Model):
    codvictima = models.AutoField(db_column='codVictima', primary_key=True)  # Field name made lowercase.
    sexo = models.CharField()
    edad = models.IntegerField(blank=True, null=True)
    extraccion = models.ForeignKey(Extraccion, models.DO_NOTHING, db_column='extraccion')
    incidente = models.ForeignKey(Incidente, models.DO_NOTHING, db_column='incidente')
    materialrescate = models.ForeignKey(Materialrescate, models.DO_NOTHING, db_column='materialRescate')  # Field name made lowercase.
    nacionalidad = models.ForeignKey(Nacionalidad, models.DO_NOTHING, db_column='nacionalidad')
    origen = models.ForeignKey(Origen, models.DO_NOTHING, db_column='origen')
    primerinterviniente = models.ForeignKey(Primerinterviniente, models.DO_NOTHING, db_column='primerInterviniente')  # Field name made lowercase.
    pronostico = models.ForeignKey(Pronostico, models.DO_NOTHING, db_column='pronostico')
    reanimacion = models.ForeignKey(Reanimacion, models.DO_NOTHING, db_column='reanimacion')
    tipoahogamiento = models.ForeignKey(Tipoahogamiento, models.DO_NOTHING, db_column='tipoAhogamiento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Victima'


class Zonavigilada(models.Model):
    codzonavigilada = models.AutoField(db_column='codZonaVigilada', primary_key=True)  # Field name made lowercase.
    nombrezonavigilada = models.CharField(db_column='nombreZonaVigilada')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZonaVigilada'

    def __str__(self):
        return self.nombrezonavigilada


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
