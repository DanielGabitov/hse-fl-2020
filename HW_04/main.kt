import java.io.File
import java.lang.Math.max
import kotlin.Pair
import kotlin.text.Regex

var best = - 1;

fun is_over_string_edge(data: String, index: Int): Boolean{
  return index >= data.length
}

fun parse_literal(data: String, state: Pair<Boolean, Int>) : Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index + 1)){
    return Pair(false, index)
  }

  val regex  = Regex("[a-z]")
  val symbol = data[index + 1].toString()

  if (regex.containsMatchIn(symbol)){
    return Pair(true, index + 1)
  }

  return Pair(false, index)
}

fun parse_symbol(data: String, state: Pair<Boolean, Int>, symbol: Char) : Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index + 1)){
    return Pair(false, index)
  }

  if (data[index + 1] == symbol){
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

  if (item_result.first){
    best = max(best, item_result.second)
  }
  if (sep_result.first){
    best = max(best, sep_result.second)
  }
  if (bracets_result.first){
    best = max(best, bracets_result.second)
  }

  if (bracets_result.first){
    return bracets_result
  }
  if (sep_result.first){
    return Pair(false, sep_result.second)
  }
  item_result = parse_item(data, state)

  if (item_result.first){
    return item_result
  }
  return Pair(false, max(item_result.second, bracets_result.second))
}

fun parse_p(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  val literal_result = parse_literal(data, state)

  if (literal_result.first){
    return literal_result
  }

  val open_bracket_result = parse_symbol(data, state, '(')
  val e_result = parse_e(data, open_bracket_result)
  val close_bracket_result = parse_symbol(data, e_result, ')')

  if (open_bracket_result.first){
    best = max(best, open_bracket_result.second)
  }

  if (e_result.first){
    best = max(best, e_result.second)
  }

  if (close_bracket_result.first){
    best = max(best, close_bracket_result.second)
  }

  if (!close_bracket_result.first){
    return Pair(false, max(literal_result.second, close_bracket_result.second))
  }

  return close_bracket_result
}

// They both are the same as parse_symbol but i need functions to give to brackets parser

fun parse_and_operator(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index + 1)){
    return Pair(false, index)
  }

  if (data[index + 1] == ','){
    return Pair(true, index + 1)
  }
  return Pair(false, index)
}

fun parse_or_operator(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  val index = state.second
  if (!state.first or is_over_string_edge(data, index + 1)){
    return Pair(false, index)
  }

  if (data[index + 1] == ';'){
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
    return Pair(false, result.second)
  }
  return result
}

fun parse_e(data: String, state: Pair<Boolean, Int>): Pair<Boolean, Int>{
  if (!state.first){
    return Pair(false, state.second)
  }
  val result = parse_brackets_r(data, state, ::parse_m, ::parse_or_operator)
  if (!result.first){
    return Pair(false, result.second)
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
  var dot_result_1   = parse_symbol(data, e_result, '.')

  if (dot_result_1.first){
    return dot_result_1
  }

  val dot_result_2 = parse_symbol(data, lit_result, '.')
  if (dot_result_2.first){
    return dot_result_2
  }
  return Pair(false, max(dot_result_1.second, dot_result_2.second))
}

fun parse(data: String): Pair<Boolean, Int>{
  val result = parse_main(data, Pair(true, -1))
  return Pair(result.first and (result.second == data.length - 1), max(result.second, best))
}


fun main(args: Array<String>) {
  val file_name = args[0]
  val file_data = File(file_name).readText()
  var data = file_data
  var array = arrayOf<String>()
  while (data.length != 0){
    if (data.indexOf('.') == -1){
      array += data
      break;
    }
    array += data.subSequence(0, data.indexOf('.') + 1).toString()
    data = data.subSequence(data.indexOf('.') + 1, data.length).toString()
  }

  var error_symbol = -2;
  var tmp = 0
  for (word in array){
    val parse_result = parse(word.filter { it != '\n' && it != ' '})
    if (!parse_result.first){
      error_symbol = parse_result.second
      break;
    }
    best = -1
    tmp += word.length
  }
  if (error_symbol == -2){
    println("Everything is correct!")
    return
  }

  var i = 0
  var colon = 0
  var line: Int
  if (tmp == 0){
    line = 1
  } else{
    line = 1 + file_data.substring(0, tmp).filter { it == '\n' }.length
  }
  data = file_data.substring(tmp, file_data.length)
  for (symbol in data){
    if (i == error_symbol + 1){
      break;
    }
    if (symbol == '\n'){
      line++
      colon = 0
    } else if (symbol == ' ') {
      colon++
    } else if (Regex("[a-z]|-|:|;|,|(|)").containsMatchIn(symbol.toString()) && symbol != ' '){
      i++
      colon++
    }
  }
  println("Syntax error: line: $line, colon: $colon.")
}
