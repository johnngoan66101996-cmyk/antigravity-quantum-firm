"""
FinOps Scorer & Scam Auditor (v9.0.0-OMEGA)
Расчет точной юнит-экономики товарного арбитража и 10 стоп-факторов аудита безопасности.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

@dataclass
class UnitEconomicsInput:
    product_name: str
    product_type: str  # "physical" или "digital"
    buy_price_donor: float  # Цена закупки у донора (руб)
    donor_logistics: float  # Доставка от донора до склада/фулфилмента (руб)
    packaging_cost: float   # Упаковка, маркировка Честный Знак, стикеровка (руб)
    sell_price_retail: float # Розничная цена продажи на витрине (руб)
    mp_fee_rate: float      # Комиссия маркетплейса/эквайринга витрины (например, 0.18 = 18%)
    acquiring_rate: float   # Эквайринг (например, 0.015 = 1.5%)
    fulfillment_cost: float # Логистика МП / ПВЗ / последняя миля (руб)
    cpa_ads_per_order: float # ДРР / Реклама на 1 выкупленный заказ (руб)
    tax_rate: float         # Ставка налога (УСН 6% = 0.06 от выручки или доходы-расходы)
    buyout_rate: float = 0.90 # Процент выкупа (0.90 для техники, 0.55 для одежды)
    defect_reserve_rate: float = 0.03 # Резерв на брак/утерю (3%)

class FinOpsScorer:
    STOP_FACTORS = [
        "1. Обещание гарантированной доходности > 100% в месяц без операционного риска.",
        "2. Требование предоплаты на криптокошелек / личную карту физлица без договора.",
        "3. Контрафакт, реплики брендов без сертификата/отказного письма.",
        "4. Запрещенные товары (оружие, фарма без лицензии, табак, серый импорт под санкциями).",
        "5. Завышенные обещания инфоцыган без документального подтверждения финотчетов.",
        "6. Дропперство, обнал чужих средств под видом «онлайн-заработка».",
        "7. Фейковые выкупы и накрутка отзывов с высоким риском пожизненного бана магазина.",
        "8. Отрицательная или нулевая юнит-экономика после вычета всех комиссий и логистики.",
        "9. Срок оборачиваемости партии более 90 дней (заморозка капитала).",
        "10. Продавец-донор зарегистрирован менее 30 дней назад, нулевой рейтинг и отзывы."
    ]

    @classmethod
    def calculate_unit_economics(cls, item: UnitEconomicsInput) -> Dict[str, Any]:
        """
        Формула:
        Net Profit per Unit = P_sell * (1 - k_mp_fee - k_acquiring) - C_fulfillment - C_ads - Taxes - Total Cost
        """
        p_sell = item.sell_price_retail
        
        # Общая себестоимость единицы (Total Cost) с учетом брака
        base_cost = item.buy_price_donor + item.donor_logistics + item.packaging_cost
        defect_cost = base_cost * item.defect_reserve_rate
        total_cost = base_cost + defect_cost
        
        # Доход после комиссии площадки и эквайринга
        revenue_after_fees = p_sell * (1.0 - item.mp_fee_rate - item.acquiring_rate)
        
        # Налог (по УСН 6% от базы реализации)
        taxes = p_sell * item.tax_rate
        
        # Логистика с поправкой на процент выкупа (обратная логистика при невыкупе)
        # Если процент выкупа r, то на 1 успешный заказ приходится (1 - r) возвратов (каждый ~ 50 руб)
        reverse_logistics = ((1.0 - item.buyout_rate) / max(item.buyout_rate, 0.1)) * 50.0
        adjusted_fulfillment = item.fulfillment_cost + reverse_logistics
        
        # Чистая прибыль на 1 единицу
        net_profit_per_unit = revenue_after_fees - adjusted_fulfillment - item.cpa_ads_per_order - taxes - total_cost
        
        # Чистая маржа (Net Margin %)
        net_margin = (net_profit_per_unit / p_sell) * 100.0 if p_sell > 0 else 0.0
        
        # ROI % на вложенный капитал (себестоимость)
        roi = (net_profit_per_unit / total_cost) * 100.0 if total_cost > 0 else 0.0
        
        # Проверка порога запуска:
        # Физические товары: маржа >= 25%
        # Цифровые товары: маржа >= 70%
        min_margin_threshold = 70.0 if item.product_type == "digital" else 25.0
        is_viable = (net_margin >= min_margin_threshold) and (net_profit_per_unit > 0)
        
        # Расчет комплексного скоринга 0-100
        score = cls._compute_finops_score(
            margin=net_margin,
            roi=roi,
            min_margin=min_margin_threshold,
            profit=net_profit_per_unit,
            buyout_rate=item.buyout_rate
        )
        
        return {
            "product_name": item.product_name,
            "product_type": item.product_type,
            "sell_price": round(p_sell, 2),
            "total_unit_cost": round(total_cost, 2),
            "fees_and_acquiring": round(p_sell * (item.mp_fee_rate + item.acquiring_rate), 2),
            "fulfillment_and_returns": round(adjusted_fulfillment, 2),
            "ads_cpa": round(item.cpa_ads_per_order, 2),
            "taxes": round(taxes, 2),
            "net_profit_per_unit": round(net_profit_per_unit, 2),
            "net_margin_percent": round(net_margin, 2),
            "roi_percent": round(roi, 2),
            "min_margin_threshold": min_margin_threshold,
            "is_viable": is_viable,
            "finops_score": score
        }

    @staticmethod
    def _compute_finops_score(margin: float, roi: float, min_margin: float, profit: float, buyout_rate: float) -> float:
        if profit <= 0 or margin <= 0:
            return 10.0
        
        # Базовый балл от превышения порога маржинальности (макс 45)
        margin_score = min(45.0, (margin / min_margin) * 35.0)
        
        # Балл от ROI (макс 35): ROI 100% дает ~30 баллов
        roi_score = min(35.0, (roi / 100.0) * 30.0)
        
        # Балл от стабильности выкупа (макс 20)
        buyout_score = buyout_rate * 20.0
        
        final_score = margin_score + roi_score + buyout_score
        return round(max(0.0, min(100.0, final_score)), 1)

    @classmethod
    def audit_stop_factors(cls, metadata: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Проверка связки на наличие стоп-факторов скама.
        Возвращает (is_clean, list_of_violations).
        """
        violations = []
        if metadata.get("guaranteed_unrealistic_yield", False):
            violations.append(cls.STOP_FACTORS[0])
        if metadata.get("crypto_p2p_prepayment", False):
            violations.append(cls.STOP_FACTORS[1])
        if metadata.get("is_counterfeit", False):
            violations.append(cls.STOP_FACTORS[2])
        if metadata.get("is_illicit_category", False):
            violations.append(cls.STOP_FACTORS[3])
        if metadata.get("fake_reviews_incentive", False):
            violations.append(cls.STOP_FACTORS[6])
        if metadata.get("negative_unit_economics", False):
            violations.append(cls.STOP_FACTORS[7])
        if metadata.get("supplier_unverified", False):
            violations.append(cls.STOP_FACTORS[9])
            
        is_clean = len(violations) == 0
        return is_clean, violations
