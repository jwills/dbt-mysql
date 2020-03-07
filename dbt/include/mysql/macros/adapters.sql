
{% macro mysql__create_table_as(temporary, relation, sql) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}

  create {% if temporary: -%}temporary{%- endif %} table
    {{ relation.include(database=(not temporary)) }}
  as (
    {{ sql }}
  );
{% endmacro %}

{% macro mysql__rename_relation(from_relation, to_relation) -%}
  {% call statement('rename_relation') -%}
    rename table {{ from_relation }} to {{ to_relation }}
  {%- endcall %}
{% endmacro %}

{% macro mysql__get_columns_in_relation(relation) -%}
  {% call statement('get_columns_in_relation', fetch_result=True) %}
      select
          column_name,
          data_type,
          character_maximum_length,
          numeric_precision,
          numeric_scale
      from information_schema.columns
      where table_name = '{{ relation.identifier }}'
        {% if relation.schema %}
        and table_schema = '{{ relation.schema }}'
        {% endif %}
      order by ordinal_position

  {% endcall %}
  {% set table = load_result('get_columns_in_relation').table %}
  {{ return(sql_convert_columns_in_relation(table)) }}
{% endmacro %}


{% macro mysql__list_relations_without_caching(information_schema, schema) %}
  {% call statement('list_relations_without_caching', fetch_result=True) -%}
    select
      table_schema as `database`,
      table_name as name,
      table_schema as `schema`,
      'table' as type
    from information_schema.tables
    where table_schema = 'dbt_test'
    union all
    select
      table_schema as `database`,
      table_name as name,
      table_schema as `schema`,
      'view' as type
    from information_schema.views
    where table_schema = 'dbt_test'
  {% endcall %}
  {{ return(load_result('list_relations_without_caching').table) }}
{% endmacro %}

