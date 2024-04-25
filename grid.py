from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode, JsCode

fmt_CurrencyRG = JsCode("""
    function(params) {
        if (params.value < 0) {    
            return {'background-color': 'red','color':'white'};
        } else {
            return {'background-color': 'green','color':'white'};
        }
    }
    """)

fmt_Currency = JsCode("""
    function(params) {
        return (params.value == null) ? params.value : "£"+params.value.toLocaleString("en-US", { maximumFractionDigits: 2, minimumFractionDigits: 2 }); 
    }
    """)

fmt_Num1dp = JsCode("""
    function(params) {
        return (params.value == null) ? params.value : params.value.toLocaleString("en-US", { maximumFractionDigits: 1, minimumFractionDigits: 1 }); 
    }
    """)

#column options for calculated columns 
CalcCol = {
    "type":['numericColumn'],
    "cellStyle": {
        'background-color': 'aliceblue'
        },  
}

v_getter = JsCode("""
    function(params) {
        if (params.data.Close_Price) {
            var output = (params.data.Close_Price - params.data.Entry_Price)*params.data.Pounds_Per_Point
        } else {
            return;
        }
        
        // write to the data to aggrid
        var col = params.colDef.field;
        params.data[col] = output;

        return output;                  
    }
    """)

def create_grid(df):
    # Configure the grid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='single', use_checkbox=False )
    gb.configure_default_column(editable=True)
    #Define calculated columns
    gb.configure_column(field='Position_Size', valueGetter='data.Pounds_Per_Point * data.Entry_Price',valueFormatter=fmt_Currency, **CalcCol)
    gb.configure_column(field='Margin', valueGetter= 'getValue("Position_Size") * .25',valueFormatter=fmt_Currency, **CalcCol)
    gb.configure_column(field='Monetary_Risk', valueGetter='(data.Entry_Price - data.Stop)*data.Pounds_Per_Point',valueFormatter=fmt_Currency, **CalcCol)
    gb.configure_column(field='P/L', valueGetter=v_getter, valueFormatter=fmt_Currency, cellStyle=fmt_CurrencyRG, type=['numericColumn'])
    gb.configure_column(field='R:R_plan', valueGetter='(data.Target - data.Entry_Price)/(data.Entry_Price - data.Stop)',valueFormatter=fmt_Num1dp, **CalcCol)
    gb.configure_side_bar()
    gridOptions = gb.build()
    
    # Display the grid
    data = AgGrid(df, gridOptions=gridOptions,
                editable=True, 
                enable_enterprise_modules=True, 
                allow_unsafe_jscode=True, 
                update_mode=GridUpdateMode.VALUE_CHANGED | GridUpdateMode.SELECTION_CHANGED, 
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
                )
    
    return data