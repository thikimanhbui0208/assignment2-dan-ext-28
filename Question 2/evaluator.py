import os

# Format numbers:
# - Remove .0 if integer
# - Otherwise round to 4 decimal places
def format_num(n):
      if isinstance(n, float):
            if n.is_integer():
                  return str(int(n))
            return f"{n:.4f}"
      return str(n)

# Tokenize Function
def tokenize (expr):
      tokens = []
      i = 0
      while i<len(expr):
            ch = expr[i]
            if ch.isspace():
                  i += 1
                  continue
            if ch.isdigit() or ch=='.':
                  start = i
                  dot_count = 0
                  while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                        if expr[i] == '.':
                              dot_count += 1
                              if dot_count > 1:
                                    raise ValueError("ERROR")
                        i += 1
                  num_text = expr[start:i]
                  if num_text == '.':
                        raise ValueError("ERROR")
                  tokens.append(("NUM",float(num_text)))
                  continue

            if ch in "+-*/":
                  tokens.append(("OP",ch))
                  i += 1
                  continue

            if ch == "(":
                  tokens.append(("LPAREN",ch))
                  i += 1
                  continue

            if ch == ")":
                  tokens.append(("RPAREN",ch))
                  i += 1
                  continue
            raise ValueError("ERROR")
      tokens.append(("END",None))
      return tokens
      
# Convert token list into required output string format
def tokens_to_string(tokens):
      parts = []
      for ttype, val in tokens:
            if ttype == "NUM":
                  parts.append(f"[NUM:{format_num(val)}]")
            elif ttype == "OP":
                  parts.append(f"[OP:{val}]")
            elif ttype == "LPAREN":
                  parts.append("[LPAREN:(]")
            elif ttype == "RPAREN":
                  parts.append("[RPAREN:)]")
            elif ttype == "END":
                  parts.append("[END]")
      return " ".join(parts)

def parse_expression(tokens,pos=0):
      return parse_add_sub(tokens,pos)

def parse_add_sub(tokens,pos):
      node,pos = parse_mul_div(tokens,pos)
      while pos < len(tokens) and tokens[pos][0] == "OP" and tokens[pos][1] in "+-":
            op = tokens[pos][1]
            rhs,pos = parse_mul_div(tokens,pos + 1)
            node = (op,node,rhs)
      return node,pos

def starts_unary_or_primary(tok):
      if tok[0] == "NUM":
            return True
      if tok[0] == "LPAREN":
            return True
      if tok[0] == "OP" and tok[1] == "-":
            return True
      return False

# Handle multiplication, division, and implicit multiplication
def parse_mul_div(tokens,pos):
      node,pos = parse_unary(tokens,pos)
      while True:
            if pos < len(tokens) and tokens[pos][0] == "OP" and tokens[pos][1]in "*/":
                  op = tokens[pos][1]
                  rhs,pos = parse_unary(tokens,pos +1)
                  node = (op,node,rhs)
            elif pos < len(tokens) and starts_unary_or_primary(tokens[pos]):
                  rhs,pos = parse_unary(tokens,pos)
                  node = ("*",node,rhs)
            else:
                  break
      return node,pos

# Handle unary negation (e.g., -x → (neg x)), reject unary +
def parse_unary(tokens,pos):
      if pos < len(tokens) and tokens[pos][0] == "OP":
            if tokens[pos][1] == "+":
                  raise ValueError("ERROR")
            if tokens[pos][1] == "-":
                  node,new_pos = parse_unary(tokens,pos+1)
                  return("neg",node),new_pos
      return parse_primary(tokens,pos)

# Handle numbers and parenthesized expressions
def parse_primary(tokens,pos):
      if pos >= len(tokens):
            raise ValueError("ERROR")
      tok_type,tok_value=tokens[pos]
      if tok_type == "NUM":
            return ("num",tok_value),pos+1
      if tok_type == "LPAREN":
            node,pos = parse_expression(tokens,pos+1)
            if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
               raise ValueError("ERROR")
            return node, pos+1
      raise ValueError("ERROR")

# Convert AST (parse tree) into required string format
def tree_to_string(node):
      kind = node[0]
      if kind == "num":
            return format_num(node[1])
      if kind == "neg":
            return f"(neg {tree_to_string(node[1])})"
      if kind in "+-*/":
            return f"({kind} {tree_to_string(node[1])} {tree_to_string(node[2])})"
      raise ValueError("ERROR")

# Evaluate AST recursively and compute final result
def eval_tree(node):
      kind = node[0]
      if kind == "num":
            return node[1]
      if kind == "neg":
            return -eval_tree(node[1])
      if kind == "+":
            return eval_tree(node[1]) + eval_tree(node[2])
      if kind == "-":
            return eval_tree(node[1]) - eval_tree(node[2])
      if kind == "*":
            return eval_tree(node[1]) * eval_tree(node[2])
      if kind == "/":
            denom = eval_tree(node[2])
            if denom == 0:
                  raise ZeroDivisionError
            return eval_tree(node[1]) / denom
      raise ValueError("ERROR")

# Main function: read input file and then write the formatted output.
def evaluate_file(input_path:str) -> list[dict]:
      results = []
      with open (input_path,"r",encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
      output_path = os.path.join(os.path.dirname(input_path),"output.txt")
      with open(output_path,"w",encoding = "utf-8") as out:
            first = True
            for line in lines:
                  expr = line.strip()
                  if expr == "":
                        continue
                  if not first:
                        out.write("\n")
                  first = False

                  try:
                        tokens = tokenize(expr)
                        tree,pos = parse_expression(tokens,0)
                        if tokens[pos][0] != "END":
                            raise ValueError("ERROR")
                        tree_str = tree_to_string(tree)
                        token_str = tokens_to_string(tokens)
                        try:
                            result_value = eval_tree(tree)
                            result_str = format_num(result_value)
                            result_store = result_value
                        except ZeroDivisionError:
                              result_str = "ERROR"
                              result_store = "ERROR"
                        item = {
                             "input" : expr,
                             "tree"  : tree_str,
                             "tokens" : token_str,
                             "result" : result_store
                        }

                        out.write(f"Input: {expr}\n")
                        out.write(f"Tree: {tree_str}\n")
                        out.write(f"Tokens: {token_str}\n")
                        out.write(f"Result: {result_str}\n")

                  except Exception:
                        item = {
                              "input": expr,
                              "tree": "ERROR",
                              "tokens": "ERROR",
                              "result":"ERROR"
                        }

                        out.write(f"Input: {expr}\n")
                        out.write(f"Tree: ERROR\n")
                        out.write(f"Tokens: ERROR\n")
                        out.write(f"Result: ERROR\n")
                  results.append(item)
      return results

if __name__ == "__main__":
      evaluate_file("input.txt") 
      print("You can check output.txt in the same folder")