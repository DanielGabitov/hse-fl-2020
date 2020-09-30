fun read_lines(): String {
  var data: String = ""
  var buffer: String? = readLine()
  while (buffer != null) {
    data += buffer
    buffer = readLine()
  }
  return data
}

fun delete_spaces(data: String): String {
  return data.filter { it != '\n' && it != '\t' && it != ' ' }
}

fun is_over_string_edge(data: String, index: Int): Boolean{
  return index >= data.length
}

fun parse_literal(data: String, state: Pair<Boolean, Int>) : Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index)){
    return Pair(false, index)
  }

  val regex  = Regex("[a-z]")
  val symbol = data[index].toString()

  if (regex.containsMatchIn(symbol)){
    return Pair(true, index + 1)
  }

  return Pair(false, index)
}

fun parse_symbol(data: String, state: Pair<Boolean, Int>, symbol: Char) : Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index)){
    return Pair(false, index)
  }

  if (data[index] == symbol){
    return Pair(true, index + 1)
  }
  return Pair(false, index)
}

fun parse_brackets_r(data: String, state: Pair<Boolean, Int>,
                  parse_item: (data: String, state: Pair<Boolean,Int>) -> Pair<Boolean, Int>,
                  parse_sep : (data: String, state: Pair<Boolean,Int>) -> Pair<Boolean, Int>)
          : Pair<Boolean, Int> {

  if (!state.first){
    return Pair(false, state.second)
  }

  var item_result    =  parse_item(data, state)
  var sep_result     =  parse_sep(data, item_result)
  var bracets_result =  parse_brackets_r(data, sep_result, parse_item, parse_sep)

  if (bracets_result.first){
    return bracets_result
  }

  item_result = parse_item(data, state)

  if (item_result.first){
    return item_result
  }

  return Pair(false, state.second)
}

fun parse_p(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  val literal_result = parse_literal(data, state)

  if (literal_result.first){
    return literal_result
  }

  val open_bracket_result = parse_symbol(data, state, '(')
  val e_result = parse_e(data, open_bracket_result)
  val close_bracket_result = parse_symbol(data, e_result, ')')

  if (!close_bracket_result.first){
    return Pair(false, state.second)
  }

  return close_bracket_result
}

// They both are the same as parse_symbol but i need functions to give to brackets parser

fun parse_and_operator(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index)){
    return Pair(false, index)
  }

  if (data[index] == ','){
    return Pair(true, index + 1)
  }
  return Pair(false, index)
}

fun parse_or_operator(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index)){
    return Pair(false, index)
  }

  if (data[index] == ';'){
    return Pair(true, index + 1)
  }
  return Pair(false, index)
}

fun parse_m(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  if (!state.first){
    return Pair(false, state.second)
  }
  val result = parse_brackets_r(data, state, ::parse_p, ::parse_and_operator)
  if (!result.first){
    return Pair(false, state.second)
  }
  return result
}

fun parse_e(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  if (!state.first){
    return Pair(false, state.second)
  }
  val result = parse_brackets_r(data, state, ::parse_m, ::parse_or_operator)
  if (!result.first){
    return Pair(false, state.second)
  }
  return result
}

fun parse_main(data: String, state: Pair<Boolean, Int>) : Pair<Boolean, Int>{
  if (!state.first){
    return Pair(false, state.second)
  }
  val lit_result   = parse_literal(data, state)
  val colon_result = parse_symbol(data, lit_result, ':')
  val hyphen_result    = parse_symbol(data, colon_result, '-')
  val e_result     = parse_e(data, hyphen_result)
  var dot_result   = parse_symbol(data, e_result, '.')

  if (dot_result.first){
    return dot_result
  }

  dot_result = parse_symbol(data, lit_result, '.')
  if (dot_result.first){
    return dot_result
  }
  return Pair(false, state.second)
}

fun parse(data: String): Boolean{
  val result = parse_main(data, Pair(true, 0))
  return result.first and (result.second == data.length)
}

fun main() {
  var data = delete_spaces(read_lines())
  when (parse(data)){
    true  -> println("YES")
    false -> println("NO")
  }
}
