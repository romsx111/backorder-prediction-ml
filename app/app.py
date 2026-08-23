from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Material Risk Planner",
    page_icon="📦",
    layout="wide",
)


# ---------------------------------------------------------
# Visual styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    /* Main page width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main title */
    h1 {
        color: #177E89;
        font-weight: 700;
    }

    /* Section headers */
    h2, h3 {
        font-weight: 600;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: rgba(23, 126, 137, 0.06);
        border: 1px solid rgba(23, 126, 137, 0.18);
        border-radius: 10px;
        padding: 14px;
    }

    /* Reduce excessive whitespace */
    div[data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[1]

    possible_paths = [
	project_root / "app" / "backorder_dashboard_sample.csv",
        project_root / "data" / "processed" / "backorder_dashboard.csv",
        project_root / "data" / "backorder_dashboard.csv",
        project_root / "backorder_dashboard.csv",
    ]

    for path in possible_paths:
        if path.exists():
            return pd.read_csv(path, low_memory=False)

    raise FileNotFoundError(
        "Could not find backorder_dashboard.csv. "
        "Check that the file is inside the project data folder."
    )


df = load_data()


# ---------------------------------------------------------
# App header
# ---------------------------------------------------------

st.title("📦 Material Risk Planner")

st.caption(
    "SKU-level backorder risk assessment and material planning decision support"
)

st.success(
    f"Dataset loaded successfully — {len(df):,} SKUs available"
)

with st.expander("Preview data"):
    st.dataframe(
        df.head(),
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# Main navigation
# ---------------------------------------------------------

tab1, tab2 = st.tabs(
    [
        "🔎 SKU Consultation",
        "🏭 BOM Risk Check",
    ]
)


# =========================================================
# TAB 1 — SKU CONSULTATION
# =========================================================

with tab1:

    st.subheader("🔎 SKU Status Consultation")

    st.caption(
        "Search for a material to review its backorder risk "
        "and current planning status."
    )

    sku_list = sorted(
        df["sku"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_sku = st.selectbox(
        "Select SKU",
        options=sku_list,
        index=None,
        placeholder="Search SKU...",
    )

    if selected_sku:

        sku_data = (
            df[df["sku"].astype(str) == selected_sku]
            .iloc[0]
        )


        # -------------------------------------------------
        # Material Status
        # -------------------------------------------------

        st.write("### Material Status")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Backorder Probability",
                f"{sku_data['backorder_probability']:.2%}",
            )

        with col2:
            st.metric(
                "Risk Level",
                sku_data["risk_level"],
            )

        with col3:
            st.metric(
                "Planner Priority",
                sku_data["planner_priority"],
            )


        # -------------------------------------------------
        # Inventory & Demand
        # -------------------------------------------------

        st.divider()

        st.subheader("📊 Inventory & Demand")

        inv1, inv2, inv3, inv4 = st.columns(4)

        with inv1:
            st.metric(
                "Current Inventory",
                f"{sku_data['national_inv']:,.0f}",
            )

        with inv2:
            st.metric(
                "In Transit Qty",
                f"{sku_data['in_transit_qty']:,.0f}",
            )

        with inv3:
            st.metric(
                "Local BO Qty",
                f"{sku_data['local_bo_qty']:,.0f}",
            )

        with inv4:
            st.metric(
                "Min Bank",
                f"{sku_data['min_bank']:,.0f}",
            )


        dem1, dem2, dem3 = st.columns(3)

        with dem1:
            st.metric(
                "3M Forecast",
                f"{sku_data['forecast_3_month']:,.0f}",
            )

        with dem2:
            st.metric(
                "6M Forecast",
                f"{sku_data['forecast_6_month']:,.0f}",
            )

        with dem3:
            st.metric(
                "9M Forecast",
                f"{sku_data['forecast_9_month']:,.0f}",
            )


        # -------------------------------------------------
        # Supply & Planning
        # -------------------------------------------------

        st.subheader("🚚 Supply & Planning")

        sup1, sup2, sup3, sup4 = st.columns(4)

        with sup1:
            st.metric(
                "Lead Time",
                f"{sku_data['lead_time']:.0f} days",
            )

        with sup2:

            supplier_perf = sku_data["perf_6_month_avg"]

            if pd.isna(supplier_perf):
                supplier_perf_display = "N/A"
            else:
                supplier_perf_display = f"{supplier_perf:.1%}"

            st.metric(
                "Supplier Performance (6M)",
                supplier_perf_display,
            )

        with sup3:
            st.metric(
                "Pieces Past Due",
                f"{sku_data['pieces_past_due']:,.0f}",
            )

        with sup4:

            actual_bo = (
                "Yes"
                if sku_data["actual_backorder"] == 1
                else "No"
            )

            st.metric(
                "Actual Backorder",
                actual_bo,
            )


        # -------------------------------------------------
        # Planner Recommendation
        # -------------------------------------------------

        st.divider()

        st.subheader("💡 Planner Recommendation")

        priority = (
            str(sku_data["planner_priority"])
            .strip()
            .lower()
        )

        risk = (
            str(sku_data["risk_level"])
            .strip()
            .lower()
        )

        if (
            priority in ["critical", "urgent", "priority review"]
            or risk == "high"
        ):

            st.error(
                "🔴 URGENT ACTION — High backorder risk detected. "
                "Review inventory availability, open supply and "
                "supplier constraints immediately."
            )

        elif (
            priority in ["high", "priority"]
            or risk == "elevated"
        ):

            st.warning(
                "🟠 PRIORITY REVIEW — Material requires planner attention. "
                "Review inventory position, incoming supply and "
                "demand requirements."
            )

        elif risk == "moderate":

            st.warning(
                "🟡 MONITOR — Moderate backorder risk detected. "
                "Monitor inventory coverage and upcoming "
                "supply requirements."
            )

        else:

            st.success(
                "🟢 ROUTINE — No immediate planner action required."
            )

    else:

        st.info(
            "Select a SKU above to view its material risk "
            "and planning status."
        )


# =========================================================
# TAB 2 — BOM / PRODUCTION MATERIAL RISK CHECK
# =========================================================

with tab2:

    # -----------------------------------------------------
    # Demo SKUs
    # -----------------------------------------------------

    with st.expander("🧪 Demo SKUs by Risk Level"):

        test_skus = (
            df[
                df["risk_level"].isin(
                    [
                        "High",
                        "Elevated",
                        "Moderate",
                        "Low",
                    ]
                )
            ]
            .groupby(
                "risk_level",
                group_keys=False,
            )
            .head(3)[
                [
                    "sku",
                    "risk_level",
                    "backorder_probability",
                    "planner_priority",
                ]
            ]
            .sort_values(
                "backorder_probability",
                ascending=False,
            )
        )

        st.dataframe(
            test_skus,
            use_container_width=True,
            hide_index=True,
        )


    # -----------------------------------------------------
    # BOM / Production Risk Check
    # -----------------------------------------------------

    st.header("🏭 BOM / Production Material Risk Check")

    st.caption(
        "Enter the SKUs required for production to identify "
        "materials that may jeopardize the production plan."
    )

    bom_input = st.text_area(
        "Enter SKU IDs",
        placeholder="Example: 1111667, 1390420, 1777175",
        help="Enter multiple SKU IDs separated by commas.",
    )


    if bom_input:

        bom_skus = [
            sku.strip()
            for sku in bom_input.split(",")
            if sku.strip()
        ]

        # Remove duplicated SKU entries typed by the user
        bom_skus = list(dict.fromkeys(bom_skus))

        bom_results = df[
            df["sku"]
            .astype(str)
            .isin(bom_skus)
        ].copy()

        missing_skus = sorted(
            set(bom_skus)
            - set(
                bom_results["sku"]
                .astype(str)
            )
        )


        # -------------------------------------------------
        # Production Readiness
        # -------------------------------------------------

        st.subheader("Production Readiness")

        total_requested = len(bom_skus)
        total_found = len(bom_results)

        high_risk = bom_results[
            bom_results["risk_level"]
            .astype(str)
            .str.lower()
            == "high"
        ]

        elevated_risk = bom_results[
            bom_results["risk_level"]
            .astype(str)
            .str.lower()
            == "elevated"
        ]

        moderate_risk = bom_results[
            bom_results["risk_level"]
            .astype(str)
            .str.lower()
            == "moderate"
        ]

        critical_count = len(high_risk)
        review_count = len(elevated_risk)
        monitor_count = len(moderate_risk)


        if critical_count > 0:

            st.error(
                f"🔴 AT RISK — {critical_count} critical material(s) "
                "may jeopardize production."
            )

        elif review_count > 0:

            st.warning(
                f"🟠 REVIEW REQUIRED — {review_count} material(s) "
                "require planner attention."
            )

        elif monitor_count > 0:

            st.warning(
                f"🟡 MONITOR — {monitor_count} material(s) "
                "show moderate backorder risk."
            )

        else:

            st.success(
                "🟢 READY — No immediate material risk detected "
                "for the selected production requirements."
            )


        # -------------------------------------------------
        # BOM KPIs
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "SKUs Requested",
                total_requested,
            )

        with col2:
            st.metric(
                "SKUs Found",
                total_found,
            )

        with col3:
            st.metric(
                "High Risk",
                critical_count,
            )

        with col4:
            st.metric(
                "Require Review",
                review_count + monitor_count,
            )


        if missing_skus:

            st.warning(
                "The following SKU IDs were not found in the dataset: "
                + ", ".join(missing_skus)
            )


        # -------------------------------------------------
        # BOM Priority Table
        # -------------------------------------------------

        st.divider()

        st.subheader("📋 Material Risk Prioritization")

        if not bom_results.empty:

            # Use actual column names from backorder_dashboard.csv
            display_columns = [
                "sku",
                "risk_level",
                "backorder_probability",
                "planner_priority",
                "national_inv",
                "inventory_gap",
                "lead_time",
                "perf_6_month_avg",
            ]

            available_columns = [
                col
                for col in display_columns
                if col in bom_results.columns
            ]

            bom_display = (
                bom_results[available_columns]
                .copy()
            )

            # Operational risk ranking
            risk_order = {
                "High": 4,
                "Elevated": 3,
                "Moderate": 2,
                "Low": 1,
            }

            bom_display["risk_rank"] = (
                bom_display["risk_level"]
                .map(risk_order)
                .fillna(0)
            )

            # Highest-risk materials first
            bom_display = (
                bom_display
                .sort_values(
                    by=[
                        "risk_rank",
                        "backorder_probability",
                    ],
                    ascending=[
                        False,
                        False,
                    ],
                )
                .drop(
                    columns="risk_rank"
                )
            )

            # Friendly column names
            bom_display = bom_display.rename(
                columns={
                    "sku": "SKU",
                    "risk_level": "Risk Level",
                    "backorder_probability": "BO Probability",
                    "planner_priority": "Planner Priority",
                    "national_inv": "Current Inventory",
                    "inventory_gap": "Inventory Gap",
                    "lead_time": "Lead Time",
                    "perf_6_month_avg": "Supplier Performance (6M)",
                }
            )

            # Format probability as percentage string
            if "BO Probability" in bom_display.columns:

                bom_display["BO Probability"] = (
                    bom_display["BO Probability"]
                    .map(
                        lambda x: (
                            f"{x:.1%}"
                            if pd.notna(x)
                            else "N/A"
                        )
                    )
                )

            if (
                "Supplier Performance (6M)"
                in bom_display.columns
            ):

                bom_display[
                    "Supplier Performance (6M)"
                ] = (
                    bom_display[
                        "Supplier Performance (6M)"
                    ]
                    .map(
                        lambda x: (
                            f"{x:.1%}"
                            if pd.notna(x)
                            else "N/A"
                        )
                    )
                )

            st.dataframe(
                bom_display,
                use_container_width=True,
                hide_index=True,
            )


        # -------------------------------------------------
        # Planner Recommended Actions
        # -------------------------------------------------

        st.divider()

        st.subheader("🎯 Recommended Planner Actions")


        if not bom_results.empty:

            immediate_review = bom_results[
                bom_results["risk_level"]
                .isin(
                    [
                        "High",
                        "Elevated",
                    ]
                )
            ].copy()

            monitor_risk = bom_results[
                bom_results["risk_level"]
                == "Moderate"
            ].copy()


            if len(immediate_review) > 0:

                st.error(
                    f"🚨 {len(immediate_review)} material(s) "
                    "require immediate planner review."
                )

                for _, row in immediate_review.iterrows():

                    sku = row["sku"]
                    risk = row["risk_level"]
                    probability = row["backorder_probability"]

                    st.markdown(
                        f"""
**SKU {sku} — {risk} Risk ({probability:.1%})**

Recommended action:
- Review available inventory and open supply.
- Check outstanding or past-due supplier deliveries.
- Validate upcoming demand requirements.
- Consider expediting, reallocating stock, or adjusting the production plan.
"""
                    )


            elif len(monitor_risk) > 0:

                st.warning(
                    f"⚠️ {len(monitor_risk)} material(s) "
                    "should be monitored."
                )

                st.write(
                    "Review inventory coverage and incoming supply "
                    "before confirming production requirements."
                )


            else:

                st.success(
                    "✅ No critical material risks detected. "
                    "Production requirements appear supported "
                    "by the selected SKUs."
                )


    else:

        st.info(
            "Enter one or more SKU IDs above to assess "
            "production material risk."
        )