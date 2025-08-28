import streamlit as st
import time

st.set_page_config(page_title="2進法の加算と減算", page_icon="🔢", layout="wide")

st.title("2進法の加算と減算を体験的に学ぶ")
st.caption("Created by Dit-Lab.(Daiki ITO)")
st.caption("Supported by Tomoaki ATSUMI")

st.markdown("""
このアプリケーションでは、コンピュータ内部で行われている2進法の計算を筆算形式で体験できます。
10進法とは少し違う「繰り上がり」と「桁借り」のルールを直感的に理解しましょう。
""")

# 2進法の加算セクション
st.markdown("## 体験1：2進法の加算（足し算）")
st.markdown("### 目的")
st.markdown("「1+1=10」となり、上の桁に「1」が繰り上がる様子を視覚的に体験します。")

col1, col2 = st.columns(2)

with col1:
    num1_add = st.text_input("1つ目の8ビット2進数", value="01011010", key="add1")
    num2_add = st.text_input("2つ目の8ビット2進数", value="01101011", key="add2")

with col2:
    st.markdown("#### 入力のヒント")
    st.markdown("- 8桁の2進数を入力してください（0と1のみ）")
    st.markdown("- 例: 01011010")

if st.button("筆算で計算する", key="calc_add"):
    if all(c in '01' for c in num1_add) and all(c in '01' for c in num2_add) and len(num1_add) == 8 and len(num2_add) == 8:
        st.markdown("### 計算過程")
        
        # 2進数を整数に変換
        n1 = int(num1_add, 2)
        n2 = int(num2_add, 2)
        result = n1 + n2
        result_bin = format(result, '08b')
        
        # 繰り上がりの計算
        carry = [0] * 9  # 9桁（最上位の繰り上がり含む）
        result_digits = []
        
        for i in range(7, -1, -1):  # 右から左へ
            digit_sum = int(num1_add[i]) + int(num2_add[i]) + carry[i+1]
            if digit_sum >= 2:
                carry[i] = 1
                result_digits.insert(0, str(digit_sum % 2))
            else:
                result_digits.insert(0, str(digit_sum))
        
        # 筆算の表示
        st.code(f"""
繰り上がり: {''.join(['1' if carry[i] else ' ' for i in range(8)])}
     {num1_add}
+)   {num2_add}
----------------
     {''.join(result_digits)}
""")
        
        # ステップ解説
        st.markdown("#### 各桁の計算:")
        for i in range(7, -1, -1):
            digit1 = int(num1_add[i])
            digit2 = int(num2_add[i])
            carry_in = carry[i+1]
            total = digit1 + digit2 + carry_in
            
            if carry_in > 0:
                st.write(f"桁{7-i+1}: {digit1} + {digit2} + {carry_in}(繰り上がり) = {total} → {total % 2} (繰り上がり: {1 if total >= 2 else 0})")
            else:
                st.write(f"桁{7-i+1}: {digit1} + {digit2} = {total} → {total % 2} {'(1繰り上がり)' if total >= 2 else ''}")
        
        final_result = ''.join(result_digits)
        if len(final_result) > 8:
            final_result = final_result[-8:]  # 8ビットに切り詰め
        
        st.success(f"答え: {final_result}")
        st.info("**ポイント**: 2進数の足し算では、「1」が2つ揃うと、その桁は「0」になり、1つ上の桁へ「1」が繰り上がります。")
    else:
        st.error("8桁の2進数（0と1のみ）を入力してください。")

st.markdown("---")
st.markdown("## 体験2：2進法の減算（引き算）")
st.markdown("### 目的")
st.markdown("「0-1」を計算するために、上の桁から「1」を借りてくると「2」として計算される「桁借り」の仕組みを体験します。")

col1, col2 = st.columns(2)

with col1:
    num1_sub = st.text_input("被減数（4ビット2進数）", value="1011", key="sub1")
    num2_sub = st.text_input("減数（4ビット2進数）", value="0101", key="sub2")

with col2:
    st.markdown("#### 入力のヒント")
    st.markdown("- 4桁の2進数を入力してください（0と1のみ）")
    st.markdown("- 被減数 ≥ 減数になるようにしてください")

if st.button("筆算で計算する", key="calc_sub"):
    if all(c in '01' for c in num1_sub) and all(c in '01' for c in num2_sub) and len(num1_sub) == 4 and len(num2_sub) == 4:
        n1 = int(num1_sub, 2)
        n2 = int(num2_sub, 2)
        
        if n1 >= n2:
            st.markdown("### 計算過程")
            
            # 桁借りの計算
            digits1 = [int(d) for d in num1_sub]
            digits2 = [int(d) for d in num2_sub]
            borrow = [0] * 4
            result_digits = []
            
            for i in range(3, -1, -1):  # 右から左へ
                if digits1[i] - borrow[i] >= digits2[i]:
                    result_digits.insert(0, str(digits1[i] - borrow[i] - digits2[i]))
                else:
                    # 桁借りが必要
                    if i > 0:
                        borrow[i-1] = 1
                        result_digits.insert(0, str(digits1[i] - borrow[i] + 2 - digits2[i]))
                    else:
                        result_digits.insert(0, str(digits1[i] - borrow[i] - digits2[i]))
            
            # 桁借りの表示
            borrow_display = ''.join(['1' if borrow[i] else ' ' for i in range(4)])
            
            st.code(f"""
桁借り:  {borrow_display}
     {num1_sub}
-)   {num2_sub}
----------------
     {''.join(result_digits)}
""")
            
            # ステップ解説
            st.markdown("#### 各桁の計算:")
            temp_digits1 = [int(d) for d in num1_sub]
            temp_borrow = [0] * 4
            
            for i in range(3, -1, -1):
                current_digit = temp_digits1[i] - temp_borrow[i]
                sub_digit = digits2[i]
                
                if current_digit >= sub_digit:
                    st.write(f"桁{4-i}: {current_digit} - {sub_digit} = {current_digit - sub_digit}")
                else:
                    if i > 0:
                        temp_borrow[i-1] = 1
                        st.write(f"桁{4-i}: {current_digit} - {sub_digit} = 桁借りして (2 + {current_digit}) - {sub_digit} = {2 + current_digit - sub_digit}")
                    else:
                        st.write(f"桁{4-i}: {current_digit} - {sub_digit} = {current_digit - sub_digit}")
            
            st.success(f"答え: {''.join(result_digits)}")
            st.info("**ポイント**: 2進数の引き算で上の桁から「1」を借りてくると、その桁では「1」が2つあるものとして計算します。「10 - 1 = 1」と考えるのがコツです。")
        else:
            st.error("被減数は減数以上である必要があります。")
    else:
        st.error("4桁の2進数（0と1のみ）を入力してください。")

st.markdown("---")
st.markdown("## おまけ：シフト演算")
st.markdown("### 目的")
st.markdown("2進数を左右にずらす「シフト演算」が、掛け算や割り算とどう関係しているのかを体験します。")

col1, col2 = st.columns(2)

with col1:
    num_shift = st.text_input("8ビット2進数", value="00101000", key="shift")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        left_shift = st.button("左へ1ビットシフト", key="left_shift")
    with col_btn2:
        right_shift = st.button("右へ1ビットシフト", key="right_shift")

with col2:
    st.markdown("#### シフト演算とは？")
    st.markdown("- **左シフト**: 全ビットを左に移動、右端に0を補充")
    st.markdown("- **右シフト**: 全ビットを右に移動、左端に0を補充")
    st.markdown("- 左シフト1回 = 2倍、右シフト1回 = 1/2")

if left_shift and all(c in '01' for c in num_shift) and len(num_shift) == 8:
    st.markdown("### 左シフト演算")
    original_val = int(num_shift, 2)
    shifted = num_shift[1:] + '0'  # 左シフト
    shifted_val = int(shifted, 2)
    
    st.code(f"""
元の数:     {num_shift} (10進数: {original_val})
左シフト後: {shifted} (10進数: {shifted_val})
""")
    
    st.success(f"左に1ビットシフトすると、{original_val} → {shifted_val} になりました！")
    if shifted_val == original_val * 2:
        st.info("左に1ビットシフトすると、元の数が2倍になりました！")
    
elif right_shift and all(c in '01' for c in num_shift) and len(num_shift) == 8:
    st.markdown("### 右シフト演算")
    original_val = int(num_shift, 2)
    shifted = '0' + num_shift[:-1]  # 右シフト
    shifted_val = int(shifted, 2)
    
    st.code(f"""
元の数:     {num_shift} (10進数: {original_val})
右シフト後: {shifted} (10進数: {shifted_val})
""")
    
    st.success(f"右に1ビットシフトすると、{original_val} → {shifted_val} になりました！")
    if shifted_val == original_val // 2:
        st.info("右に1ビットシフトすると、元の数が1/2になりました！")

elif (left_shift or right_shift) and not (all(c in '01' for c in num_shift) and len(num_shift) == 8):
    st.error("8桁の2進数（0と1のみ）を入力してください。")

st.info("**ポイント**: 2進数の世界では、桁を1つ左にずらす（シフトする）だけで、簡単に元の数を2倍にできます。これはコンピュータが高速に掛け算を行うための重要なテクニックです。")

# 追加の学習コンテンツ
st.markdown("---")
st.markdown("## さらに学習を深めるために")

st.markdown("### 2進数と10進数の変換練習")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 2進数 → 10進数")
    bin_to_dec_input = st.text_input("2進数を入力", value="1010", key="bin_to_dec")
    if st.button("10進数に変換", key="convert_to_dec"):
        if all(c in '01' for c in bin_to_dec_input):
            decimal_val = int(bin_to_dec_input, 2)
            st.success(f"2進数 {bin_to_dec_input} = 10進数 {decimal_val}")
            
            # 計算過程を表示
            st.markdown("**計算過程:**")
            calculation = []
            for i, digit in enumerate(reversed(bin_to_dec_input)):
                if digit == '1':
                    calculation.append(f"{digit} × 2^{i} = {2**i}")
                else:
                    calculation.append(f"{digit} × 2^{i} = 0")
            
            st.write(" + ".join(calculation) + f" = {decimal_val}")
        else:
            st.error("0と1のみで構成された2進数を入力してください。")

with col2:
    st.markdown("#### 10進数 → 2進数")
    dec_to_bin_input = st.number_input("10進数を入力", min_value=0, max_value=255, value=10, key="dec_to_bin")
    if st.button("2進数に変換", key="convert_to_bin"):
        binary_val = format(dec_to_bin_input, 'b')
        st.success(f"10進数 {dec_to_bin_input} = 2進数 {binary_val}")
        
        # 計算過程を表示
        st.markdown("**計算過程（2で割り続ける方法）:**")
        temp = dec_to_bin_input
        steps = []
        while temp > 0:
            remainder = temp % 2
            temp = temp // 2
            steps.append(f"{temp * 2 + remainder} ÷ 2 = {temp} 余り {remainder}")
        
        for step in steps:
            st.write(step)
        st.write(f"余りを下から読むと: {binary_val}")

st.markdown("---")
st.markdown("### もっと大きな数で練習")
st.markdown("#### 16ビット演算にチャレンジ")
st.markdown("より大きな数での2進法演算を体験してみましょう！")

col1, col2 = st.columns(2)

with col1:
    big_num1 = st.text_input("16ビット2進数 1", value="0001101010110100", key="big1")
    big_num2 = st.text_input("16ビット2進数 2", value="0010110101001011", key="big2")

with col2:
    operation = st.radio("演算を選択", ["加算", "減算"], key="big_op")

if st.button("大きな数で計算", key="big_calc"):
    if (all(c in '01' for c in big_num1) and all(c in '01' for c in big_num2) and 
        len(big_num1) == 16 and len(big_num2) == 16):
        
        val1 = int(big_num1, 2)
        val2 = int(big_num2, 2)
        
        if operation == "加算":
            result = val1 + val2
            result_bin = format(result, '016b')
            st.code(f"""
{big_num1} ({val1})
+)  {big_num2} ({val2})
{'='*34}
{result_bin} ({result})
""")
            st.success(f"16ビット加算の結果: {result_bin}")
            
        else:  # 減算
            if val1 >= val2:
                result = val1 - val2
                result_bin = format(result, '016b')
                st.code(f"""
{big_num1} ({val1})
-)  {big_num2} ({val2})
{'='*34}
{result_bin} ({result})
""")
                st.success(f"16ビット減算の結果: {result_bin}")
            else:
                st.error("被減数は減数以上である必要があります。")
    else:
        st.error("16桁の2進数（0と1のみ）を入力してください。")

st.markdown("---")
st.markdown("### 🎓 学習のまとめ")
st.markdown("""
- **2進法の加算**: 1+1=10（繰り上がり）のルールを理解
- **2進法の減算**: 桁借りで「10-1=1」として計算
- **シフト演算**: 左シフトで2倍、右シフトで1/2
- **コンピュータの世界**: 全て0と1の組み合わせで表現

これらの基礎を理解することで、コンピュータがどのように計算を行っているかがわかります！
""")